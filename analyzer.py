'''
Due on Feb 22, 2014
CS4480-001
@author: Joseph Lee

Web Proxy Server
'''

#NOTE FOR TA
#THIS CODE WAS USED FOR DEBUGGING ONLY
#IF YOU WANT TO ENABLE THIS, SET THE FLAG IN
#proxy_server.py for do_analytics = True
#OR ELSE THIS WILL BE SKIPPED ENTIRELY

class analyzer(object):
    '''
    classdocs
    '''
    
    #contains data for open sockets
    open_sockets = {}
    #contains data for closed sockets
    closed_sockets = {}
    #contains data for open files
    open_files = {}
    #contains data for closed files
    closed_files = {}
    
    #opened socket count
    sockets_opened = 0
    #opened file count
    files_opened = 0
    #closed socket count
    sockets_closed = 0
    #closed file countt
    files_closed = 0
    
    '''
    This code is used for debugging purposes only
    '''
    def __init__(self):
        print("Analyzer Initialized")
        
    def open_sock(self, sock, host, type):
        self.open_sockets[sock] = (host, type)
        self.sockets_opened += 1
        
    def open_file(self, file, filename, type):
        self.open_files[file] = (filename, type)
        self.files_opened += 1
        
    def close_sock(self, sock):
        if(sock in self.open_sockets):
            self.closed_sockets[sock] = self.open_sockets[sock]
            self.open_sockets.pop(sock)
            self.sockets_closed += 1
        
    def close_file(self, file):
        if(file in self.open_files):
            self.closed_files[file] = self.open_files[file]
            self.open_files.pop(file)
            self.files_closed += 1
            
    def display_analytics(self):
        print("**** ANALYTICS **************")
        self._display_open_socks()
        print("    Files Opened:", self.files_opened)
        print("    Files Closed:", self.files_closed)
        print("    Sockets Opened:", self.sockets_opened)
        print("    Sockets Closed:", self.sockets_closed)
        
        print("**** END ANALYTICS **********")
        
    def _display_open_socks(self):
        print("    *** SOCKETS STILL OPEN:")
        for sock in self.open_sockets:
            print("        ", self.open_sockets[sock])
        