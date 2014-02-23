'''
Created on Jan 24, 2014

@author: Joseph Lee
'''
from os import path
import sys
import re
import string
#import socket

class cache_manager(object):
    '''
    controls the file manage for caching
    '''
    
    #the file object
    file = None
    file_socket = None
    
    '''
    Constructor
    @param filename: the filename to open
    '''
    def __init__(self, filename, analyze, do_analytics):
        #set the filepath
        self.filepath = "cache/" + self._strip(filename) + '.txt'
        self.analyze = analyze
        self.do_analytics = do_analytics
        

    #opens the file if exists or creates
    def try_open_file(self):
        if self.file == None:
            try:
                #file exists, open and return true
                self.file = open(self.filepath, 'r+')
                if(do_analytics):
                    self.analyze.open_file(file, self.filepath, "read_only")
                return 1
            except:
                #file doesn't exist, open and return false
                return 0
    
    '''
    Close the file
    '''            
    def close_file(self):
        if self.file != None:
            if(self.do_analytics):
                self.analyze.close_file(self.file)
            self.file.close()
            self.file = None
        if self.file_socket != None:
            if(self.do_analytics):
                self.analyze.close_file(self.file_socket)
            self.file_socket.close()
            self.file_socket = None
    
    '''
    Used to send Get requests to the socket file_socket
    '''
    def make_socket_file(self, socket, send_data):
        self.file_socket = socket.makefile('r', 0)
        self.file_socket.write(send_data)
        self.file = open(self.filepath, 'w+')
        if(self.do_analytics):
            self.analyze.open_file(self.file, self.filepath, "write_file")
            self.analyze.open_file(self.file_socket, self.filepath, "socket_file")
    '''
    Write the cache data to the file
    '''
    def cache_data(self, data):
        if self.file == None:
            raise Exception("Unable to cache, file not found")
        else:
            self.file.write(data)
    
    '''
    Read the data from the cache
    '''
    def read_cache(self):
        if self.file == None:
            raise Exception("Unable to read cache, file not found")
        else:
            return self.file.readlines()
    
    '''
    Strips all invalid characters from the filename
    '''
    def _strip(self, s):
        s = ''.join(e for e in s if e.isalnum())
        return s
    