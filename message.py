'''
Due on 7Feb , 2014
CS4480-001
@author: Joseph Lee

Web Proxy Server
'''

from socket import *
import sys
from queue import Queue

class Message(object):
    '''
    Message controls the sending and receiving of a message
    @param incoming is the addr to receive from
    @param outgoing is the addr to send to, if null will need to be determined
        from the message
    @param message is the message received to send
    '''
    MAX_BUFFER = 1024
    done_receiving = False
    

    def __init__(self, incoming, outgoing):
        self.incoming = incoming;
        self.outgoing = outgoing;
        self.message_queue = Queue();
        
        
    def send(self):
        #print("trying to send")
        if(self.outgoing != None):
            if(not self.message_queue.empty()):
                try:
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
        return True
    
    def recv(self):
        try:
            data = self.incoming.recv(self.MAX_BUFFER)
        except:
            return False
        #print("\t\tMessage: DataRecv:", len(data))
        if len(data) == 0:
            return False
        else:
            self.message_queue.put_nowait(data)
            return True
        
    def translate(self):
        enc_message = b""
        while(not self.message_queue.empty()):
            #construct the message
            enc_message += self.message_queue.get_nowait()
            
        #decode the data to a string
        message = ""
        try:
            message = enc_message.decode("utf-8")
            #self._print_msg(message)
        except:
            #could not be decoded, return empty strings
            return "", ""
        lines = message.split('\r\n')
        #grab the request and all headers
        rqst = lines[0]
        headers = []
        for i in range(1, len(lines)):
            headers.append(lines[i])
        return rqst, headers
    
    def _print_msg(self, msg):
        a = msg.split('\r\n')
        for x in a:
            print(x)
            
    
        