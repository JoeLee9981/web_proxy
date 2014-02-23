'''
Due on Feb 22, 2014
CS4480-001
@author: Joseph Lee

Client Socket
'''

from socket import *

class client(object):
    '''
    classdocs
    '''

    '''
    Constructor
    '''
    def __init__(self, addr, port):
        self.address = addr
        self.port = port
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        
    def start(self):
        #print('Bound to:', self.clientSocket.getsockname())
        self.clientSocket.connect((self.address, self.port))
        sentence = input('Input lowercase sentence:')
        sentence += "\r\n"
        sentence = sentence.encode('utf_8')
        self.clientSocket.send(sentence)
        print("FROM SERVER: ")
        while 1:
            data = self.clientSocket.recv(1024)
            if len(data) == 0:
                break
            print(data)
        print("Close socket")
        self.clientSocket.close()
        
        

    

        