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



class proxy_server(object):
    '''
    proxy_server encapsulates the sockets used for server management of an HTTP Proxy
    '''
    
    #a set used to get the message for outgoing
    out_queue = {}
    #a set used to get the message for incoming
    in_queue = {}
    
    '''
    Constructor
    @param adddr: is the ip address
    @param port: the port number
    '''
    def __init__(self, addr, port):
        self.port = port
        self.address = addr
        self.server = socket(AF_INET, SOCK_STREAM)
        self.server.settimeout(1)
        
    
    '''
    Start the server and perform the select loops for input and output
    '''  
    def start(self):
        #bind the socket
        print("Socket: ", self.server.fileno())
        print(self.address, self.port)
        self.server.bind((self.address, self.port))
        print("Socket Bound: ", self.server.getsockname())
        #listen for incoming connections
        self.server.listen(100)
        self.input = [self.server]
        self.output = []
        '''
        Counters (REMOVE)
        '''
        self.sockets_open = 0
        self.sockets_closed = 0
        
        while 1:
            #select sockets for input or output
            inputready,outputready,exceptready = select.select(self.input, self.output, [])
            
            for s in inputready:
                if s == self.server:
                    #new connection from server was found
                    print('Handle server socket')
                    connectionSocket, addr = self.server.accept()
                    print("Accepted connection from:", connectionSocket.getpeername())
                    self.sockets_open += 1
                    #create the message queue
                    message = Message(connectionSocket, None)
                    #add to input queue and input set
                    self.enable_input(connectionSocket, message)
                    
                else:
                    #try:
                    #socket has been closed from other end
                    if(self.in_queue[s].recv() == False):
                        #flag done and disable input
                        self.in_queue[s].done_receiving = True
                        self.disable_input(s)
                    else:
                        print("HOW OFTEN DO WE HIT HERE")
                        #data is received, and ready, add it for output
                        if(self.in_queue[s].out_ready):
                            self.enable_output(s, self.in_queue[s])
                            self.in_queue[s].done_receiving = True
                    '''
                    except:
                        print("\nException encounterd on input, closing connection\n")
                        #send bad request and cleanup
                        s.send(b"400 Bad Request")
                        s.close()
                        self.disable_input(s) '''
                        
            #Handle output
            for s in outputready:
                #try:
                if(self.out_queue[s].outgoing != None):  
                    #ready to respond back to initiating socket 
                    if(not self.out_queue[s].send()):
                        #nothing left to send, remove from output
                        print("*** Closing socket ***")
                        self.out_queue[s].end_cache()
                        self.disable_input(self.out_queue[s].outgoing)
                        self.disable_output(self.out_queue[s].outgoing)
                        self.out_queue[s].outgoing.close()
                        self.disable_input(s)
                        self.disable_output(s)
                        self.close_sock(s)
                        '''
                        Counter only REMOVE
                        '''
                        self.sockets_closed += 2
                        print("--- Sockets opened", self.sockets_open, "Sockets closed:", self.sockets_closed)
                else:
                    #try:
                    #parse the data from the queue
                    rqst, headers = self.out_queue[s].translate()
                    send_data, host, file = self.get_command(rqst, headers)
                    if(host != ""):
                        #host is valid, create the socket
                        sock = socket(AF_INET, SOCK_STREAM)
                        #check for cache
                        cache = cache_manager(host + file)
                        if(cache.try_open_file()):
                            #cache file found
                            '''
                            TODO UPDATE CACHING
                            '''
                            print("*** CACHING ****")
                            #sock.connect((host, 80))
                            #sock.connect(("localhost", 1433))
                            #self.sockets_open += 1
                            #sock.send(send_data)
                            message = Message(None, s, cache)
                            message.send_from_cache()
                            self.disable_input(s)
                            self.disable_output(s)
                            self.close_sock(s)
                        else:
                            #no cache was found, connect to socket
                            print("*** CONNECTING ****")
                            #sock.connect((host, 80))
                            sock.connect(("localhost", 1433))
                            '''
                            REMOVE THIS
                            '''
                            self.sockets_open += 1
                            #send the data
                            sock.send(send_data)
                            #create message and append new socket as input
                            message = Message(sock, s, cache)
                            self.enable_input(sock, message)
                    else:
                        #error from server, disable all
                        print("ERROR WITH HOST:", host, send_data)
                        s.send(send_data.encode('utf-8'))
                        self.disable_input(self.out_queue[s].outgoing)
                        self.disable_output(self.out_queue[s].outgoing)
                        if(self.out_queue[s].outgoing != None):
                            self.out_queue[s].outgoing.close()
                            self.sockets_closed += 1
                        self.disable_input(s)
                        self.disable_output(s)
                        self.close_sock(s)
                        self.sockets_closed += 1
                        print("--- Sockets opened", self.sockets_open, "Sockets closed:", self.sockets_closed)
                    #We are done receiving from initial socket
                    self.disable_input(s)
                    self.disable_output(s)
                    '''
                    except:
                        print("\nException encounterd on input, closing connection\n")
                        #send bad request and cleanup
                        s.send(b"400 Bad Request")
                        s.close()
                        self.disable_input(s)
                        self.disable_output(s)'''
    
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
            #self.close_sock(s)
    
    '''
    disable a socket from output
    '''
    def disable_output(self, s):
        if s in self.output:
            self.output.remove(s)
            self.out_queue.pop(s)
            #self.close_sock(s)
    
    '''
    closes a socket
    '''
    def close_sock(self, s):
        if not s in self.input and not s in self.output:
            print("Closing socket")
            s.close()
    
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
            print("*** ERROR Rqst:", rqst, "CMD:", cmd, "not recognized")
            return "501 Not Implemented\r\n\r\n", "", ""
            
    '''
    takes the request and headers and formats them into
    a string to send to the server
    '''
    def _format_send(self, rqst, headers):
        send_data = ""
        host = ""
        file = ""
        #if there is more than one header
        if len(headers) > 0:
            #format and append the request
            send_data += "GET " + rqst.split(' ')[1] + " HTTP/1.0\r\n"
            #format and append all headers
            for h in headers:
                #when the host is found save it
                if h.split(' ')[0].upper() == 'HOST:':
                    host = h.split(' ')[1]
                send_data += self._parse_header(h)
        #one line get request
        else:
            #split and format into multiline response for server
            line = rqst.split(' ')
            host, file = self._parse_url(line[1])
            send_data = "GET " + file + " HTTP/1.0\r\n"
            send_data += "Host: " + host + "\r\n"
            send_data += "Connection: close\r\n\r\n"
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
        split_line = self._clear_empty(line.split('/'))
        host = split_line[1]
        file = "/"
        for i in range(2, len(split_line)):
            file += split_line[i]
        return host, file
            
        
        