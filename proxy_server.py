'''
Due on Jan 25, 2014
CS4480-001
@author: Joseph Lee

Web Proxy Server
'''

from socket import *
import sys
import select
from cache_manager import *
from message import Message
from analyzer import analyzer



class proxy_server(object):
    '''
    proxy_server encapsulates the sockets used for server management of an HTTP Proxy
    '''
    
    #a set used to get the message for outgoing
    out_queue = {}
    #a set used to get the message for incoming
    in_queue = {}
    #list of websites cached
    cached_files = []
    
    
    #NOTE FOR TA CHANGE THESE FLAGS IF YOU WANT TO VIEW DEBUG DATA
    do_analytics = False
    show_output = False
    show_input = True
    show_file_debug = False
    
    '''
    Constructor
    @param adddr: is the ip address
    @param port: the port number
    '''
    def __init__(self, addr, port):
        self.port = port
        self.address = addr
        self.server = socket(AF_INET, SOCK_STREAM)
        self.analyze = analyzer()
        
        
    
    '''
    Start the server and perform the select loops for input and output
    '''  
    def start(self):
        #bind the socket
        print("Socket: ", self.server.fileno())
        print(self.address, self.port)
        self.server.bind((self.address, self.port))
        print("Socket Bound: ", self.server.getsockname())
        print("--------------------------------------------")
        #listen for incoming connections
        self.server.listen(100)
        self.input = [self.server]
        self.output = []


        
        while 1:
            #select sockets for input or output
            inputready,outputready,exceptready = select.select(self.input, self.output, [])
            
            for s in inputready:
                if s == self.server:
                    #new connection from server was found
                    print('Handle server socket')
                    connectionSocket, addr = self.server.accept()
                    print("Accepted connection from:", connectionSocket.getpeername())
                    #create the message queue
                    message = Message(connectionSocket, None)
                    self._enable_debug(message)
                    #add to input queue and input set
                    self.enable_input(connectionSocket, message)
                    if(self.do_analytics):
                        #set analyze
                        self.analyze.open_sock(connectionSocket, addr, "client")
                else:
                    try:
                        #socket has been closed from other end
                        if(self.in_queue[s].recv() == False):
                            #flag done and disable input
                            self.in_queue[s].done_receiving = True
                            self.disable_input(s)
                        #data is received, and ready, add it for output
                        if(self.in_queue[s].out_ready):
                            self.enable_output(s, self.in_queue[s])
                    except:
                        #send bad request and cleanup
                        s.send(b"400 Bad Request")
                        self.close_sock(s)
                        self.disable_input(s)
                        
            #Handle output
            for s in outputready:
                #try:
                if(self.out_queue[s].outgoing != None):  
                    #ready to respond back to initiating socket 
                    if(not self.out_queue[s].send()):
                        #nothing left to send, remove from output
                        self.out_queue[s].end_cache()
                        self.disable_input(self.out_queue[s].outgoing)
                        self.disable_output(self.out_queue[s].outgoing)
                        self.close_sock(self.out_queue[s].outgoing)
                        self.disable_input(s)
                        self.disable_output(s)
                        self.close_sock(s)
                else:
                    #try:
                    #parse the data from the queue
                    rqst, headers = self.out_queue[s].translate()
                    send_data, host, file = self.get_command(rqst, headers)
                    port = self._get_port(host)
                    host = self._get_host(host)
                    if(host != ""):
                        #host is valid, create the socket
                        
                        #check for cache
                        cache = cache_manager(host + file, self.analyze, self.do_analytics)
                        try:
                            if(cache.try_open_file() and (host + file) in self.cached_files):
                                #cache file found and is flagged in cached_files
                                try:
                                    message = Message(None, s, cache)
                                    self._enable_debug(message)
                                    message.send_from_cache()
                                    self.disable_input(s)
                                    self.disable_output(s)
                                    self.close_sock(s)
                                except:
                                    #error occurs reading from file, get file from host
                                    self._get_web_url(s, host, file, send_data, cache) 
                            else:
                                #no cache, get from host and add to cached_files
                                self._get_web_url(s, host, file, send_data, cache)
                                self.cached_files.append(host + file)
                        except:
                            self._get_web_url(s, host, file, send_data, None)
                    else:
                        #error from server, disable all
                        print("ERROR WITH HOST:", host, send_data)
                        #send the error
                        s.send(send_data)
                        self.out_queue[s].end_cache()
                        self.disable_input(self.out_queue[s].outgoing)
                        self.disable_output(self.out_queue[s].outgoing)
                        if(self.out_queue[s].outgoing != None):
                            self.close_sock(self.out_queue[s].outgoing)
                        self.disable_input(s)
                        self.disable_output(s)
                        self.close_sock(s)
                    #We are done receiving from initial socket
                    self.disable_input(s)
                    self.disable_output(s)
                    '''except:
                    print("\nException encounterd on input, closing connection\n")
                    #send bad request and cleanup
                    s.send(b"400 Bad Request")
                    self.close_sock(s)
                    self.disable_input(s)
                    self.disable_output(s)'''
            
            if(self.do_analytics):
                self.analyze.display_analytics()
    
    '''
    opens a socket to the web server and sends the get request
    '''
    def _get_web_url(self, s, host, file, send_data, cache):
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((host, 80))
        if(self.do_analytics):
            self.analyze.open_sock(sock, host, "web_server")
        #send the data
        if(cache != None):
            #send it through a cache file
            cache.make_socket_file(sock, send_data)
        else:
            #unable to cache, send it by normal socket
            sock.send(send_data)
        #create message and append new socket as input
        message = Message(sock, s, cache)
        self._enable_debug(message)
        self.enable_input(sock, message)
    
    '''
    closes the server
    '''
    def close(self):
        self.server.close()
        
    '''
    enable a socket for input
    '''
    def enable_input(self, s, message):
        if not s in self.input:
            self.input.append(s)
            self.in_queue[s] = message
    
    '''
    enable a socket for output
    '''
    def enable_output(self, s, message):
        if not s in self.output:
            self.output.append(s)
            self.out_queue[s] = message
    
    '''
    disable a socket from input
    '''    
    def disable_input(self, s):
        if s in self.input:
            self.input.remove(s)
            self.in_queue.pop(s)
    
    '''
    disable a socket from output
    '''
    def disable_output(self, s):
        if s in self.output:
            self.output.remove(s)
            self.out_queue.pop(s)
    
    '''
    closes a socket
    '''
    def close_sock(self, s):
        if not s in self.input and not s in self.output:
            s.close()
            if(self.do_analytics):
                self.analyze.close_sock(s)
    
    '''
    do_command checks for GET command and forwards to server
    returns the data or 501 if not valid
    '''
    def get_command(self, rqst, headers):
        headers = self._clear_empty(headers)
        cmd = rqst.split(' ')[0]
        #check for a valid command
        if cmd.upper() == 'GET':
            #format data to be sent to server
            send_data, host, file = self._format_send(rqst, headers)
            return send_data, host, file
        else:
            #invalid command, print error and return 501
            return "501 Not Implemented\r\n\r\n", "", ""
                     
    '''
    takes the request and headers and formats them into
    a string to send to the server
    '''
    def _format_send(self, rqst, headers):
        send_data = ""
        host = ""
        file = ""
        line = rqst.split(' ')
        host, file = self._parse_url(line[1])
        #if there is more than one header
        if len(headers) > 0:
            #format and append the request
            send_data += "GET " + file + " HTTP/1.0\r\n"
            #format and append all headers
            for h in headers:
                #when the host is found save it
                #if h.split(' ')[0].upper() == 'HOST:':
                    #host = h.split(' ')[1]
                send_data += self._parse_header(h)
        #one line get request
        else:
            #split and format into multiline response for server
            send_data = "GET " + file + " HTTP/1.0\r\n"
            send_data += "Host: " + host.split(":")[0] + "\r\n"
            send_data += "Connection: close\r\n"
        #append closing \r\n
        send_data += "\r\n"
        return send_data, host, file

    '''
    checks the header and formats it for the multiline
    send string
    '''
    def _parse_header(self, header):
        line = header.split(' ')
        if line[0].upper() == 'CONNECTION:':
            return "Connection: close\r\n"
        else:
            return header + "\r\n"
        
    '''
    removes empty strings from an array
    '''
    def _clear_empty(self, string_array):
        a = []
        for x in string_array:
            if x != '':
                a.append(x)
        return a
    
    '''
    parses the host and url out of a request line
    used for single line GET requests
    '''
    def _parse_url(self, line):
        line = line.replace('http://', '', 1)
        split_line = self._clear_empty(line.split('/'))
        host = split_line[0]
        file = "/"
        
        for i in range(1, len(split_line)):
            file += split_line[i]
            if(i != len(split_line) - 1):
                file += "/"
        return host, file
    
    '''
    Extract the port form the host
    '''
    def _get_port(self, host):
        port = 80
        if ':' in host:
            port = host.split(':')[1]
        return int(port)
    
    '''
    extract the host if a port is included
    '''
    def _get_host(self, host):
        if ':' in host:
            return host.split(':')[0]
        return host
    
    '''
    enables debug, set flags at the top
    '''
    def _enable_debug(self, message):
        if(self.show_output):
            message.show_output = True
        if(self.show_input):
            message.show_input = True
        if(self.show_file_debug):
            message.show_file_debug = True
        