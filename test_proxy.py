'''
Due on Jan 25, 2014
CS4480-001
@author: Joseph Lee

Web Proxy Server
'''

from socket import *
import sys
import select


class test_proxy(object):
    '''
    classdocs
    '''
    
    #contains a message for sending
    out_queue = {}
    #contains a message for receiving
    in_queue = {}
    '''
    Constructor
    '''
    def __init__(self, addr, port):
        self.port = port
        self.address = addr
        #create the socket
        self.server = socket(AF_INET, SOCK_STREAM)
        
    
    '''
    Start the server and perform the select loops for input and output
    '''  
    def start(self):
        #bind the socket
        print("Socket: ", self.server.fileno())
        self.server.bind((self.address, self.port))
        print("Socket Bound: ", self.server.getsockname())
        #listen for incoming connections
        self.server.listen(100)
        self.input = [self.server]
        self.output = []
        
        while 1:
            #print
            print("-----------------------------------------------------")
            #check for ready values
            inputready,outputready,exceptready = select.select(self.input, self.output, [])
            
            for s in inputready:
                if s == self.server:
                    #new connection from server was found
                    print('Handle server socket')
                    connectionSocket, addr = self.server.accept()
                    print("Accepted connection from:", connectionSocket.getpeername())
                    self.input.append(connectionSocket)
                else:
                    enc_data = s.recv(1024)
                    if len(enc_data) == 0:
                        s.close()
                        self.input.remove(s)
                        print("CLOSED")
                    else:
                        print("Received:", enc_data)
                        for i in range(100):
                            s.send(str(i) + ": Message\r\n     and stuff")
                            s.send(" is fun")
                            s.send(" to do\r\n")
                        s.send(b"SUCCESS\r\n\r\n")
                        #s.close()
                        #self.input.remove(s)
                    '''
                    if(len(enc_data) == 0):
                        #no data received, close socket
                        self.input.remove(s)
                        s.close()
                        print("SOCKET CLOSED")
                    else:
                        for i in range(1000):
                            msg = str(i) + " " + self.get_message()
                            s.send(msg.encode("utf-8"))
                            print("SENT:", i, self.get_message())
                        s.send( b" SUCCESS\r\n\r\n")
                        self.input.remove(s)
                        s.close() '''

    '''
    closes the server
    '''
    def close(self):
        self.server.close()                        
                        
            
    def get_message(self):
        return "This is fun\r\n"
    
    
    
def main():
    try:
        port = 1433
        s = test_proxy("localhost", port)
        s.start()
    finally:
        s.close()
        print("Closing Server")

if __name__ == '__main__':
    main()