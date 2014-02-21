'''
Due on 7Feb , 2014
CS4480-001
@author: Joseph Lee

Web Proxy Server
'''

from socket import *
import sys
from Queue import Queue

class Message(object):
    
    #maximum buffer size
    MAX_BUFFER = 1024
    #flag to check if done receiving from incoming socket
    done_receiving = False
    #cache manager controls the caching
    cache_mgr = None
    
    #flag if a cached file is found
    cache_found = False
    
    #stores an incomplete message
    incomplete_message = ""
    #set to true when output is ready
    out_ready = False
    
    '''
    Message controls the sending and receiving of a message
    @param incoming: is the addr to receive from
    @param outgoing: is the addr to send to, if null will need to be determined
        from the message
    @param cache: is the cache manager created to handle file input and output
    '''
    def __init__(self, incoming, outgoing, cache=None):
        self.incoming = incoming
        self.outgoing = outgoing
        self.message_queue = Queue()
        self.cache_mgr = cache
        
    '''
    Sends data on the outgoing socket
    ''' 
    def send(self):
        if(self.outgoing != None):
            if(not self.message_queue.empty()):
                try:
                    #attempt to send the next message in the queue
                    msg = self.message_queue.get_nowait()
                    self.outgoing.send(msg)
                    self.Failed_Send = 0
                except:
                    #send failed problem with socket return false
                    return False
            else:
                #if done receiving and queue is empty, we are done
                if self.done_receiving:
                    return False
        #send successful return true
        return True
    
    '''
    Receives data on the incoming socket
    '''
    def recv(self):
        data = b""
        '''
        if self.cache_found:
            data = self.cache_mgr.read_cache().encode('utf-8')
            print "From File:", data
        else: '''
        #try:
        #receive data up to 1024
        data = self.incoming.recv(self.MAX_BUFFER)
        #if cache manager is found store to cache
        if(self.cache_mgr != None):
            self.cache_mgr.cache_data(data)
        #except:
            #print("*** RECEIVE FAILED ***")
            #return False
            #print("\t\tMessage: DataRecv:", len(data))
        #return true or false if data was queued
        return self.queue_data(data)
    
    '''
    Checks for newline characters and adds datat to queue
    '''    
    def queue_data(self, data):
        #no data is received return false for fail
        if len(data) == 0:
            return False
        #check for newline characters in received data
        if '\r\n' in data:
            #append message and add to queue
            message = self.incomplete_message + data
            self.message_queue.put_nowait(message)
            self.incomplete_message = ""
            #We are now able to parse and add to output
            self.out_ready = True
        else:
            #no newline character, append to incomplete message
            self.incomplete_message += data
        #queue successful return true
        return True
        
        
    '''
    translates received data and returns it into the request and headers
    '''
    def translate(self):
        message = ""
        while(not self.message_queue.empty()):
            #construct the message
            message += self.message_queue.get_nowait()
        lines = message.split('\r\n')
        #grab the request and all headers
        rqst = lines[0]
        headers = []
        for i in range(1, len(lines)):
            headers.append(lines[i])
        return rqst, headers
            
    '''
    open the file to cache to
    '''
    def start_cache(self, filename):
        try:
            self.cache_found = self.cache_mgr.try_open_file()
        except:
            print("Cache failed to init")

    '''
    close the file to cache to
    '''
    def end_cache(self):
        if self.cache_mgr != None:
            self.cache_mgr.close_file()
            self.cache_mgr = None
            
    def send_from_cache(self):
        if self.cache_mgr == None:
            raise Exception("Unable to cache, invalid cache object")
        else:
            content = self.cache_mgr.read_cache()
            for line in content:
                self.outgoing.send(line.encode("utf-8"))
    
        