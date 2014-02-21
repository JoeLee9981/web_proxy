'''
Created on Jan 24, 2014

@author: god_laptop
'''
from os import path
import sys
import re
import string

class cache_manager(object):
    '''
    controls the file manage for caching
    '''
    
    #the file object
    file = None
    
    '''
    Constructor
    @param filename: the filename to open
    '''
    def __init__(self, filename):
        #set the filepath
        self.filepath = "cache/" + self._strip(filename) + '.txt'

    #opens the file if exists or creates
    def try_open_file(self):
        if self.file == None:
            try:
                #file exists, open and return true
                self.file = open(self.filepath, 'r+')
                return 1
            except:
                #file doesn't exist, open and return false
                self.file = open(self.filepath, 'w+')
                return 0
    
    '''
    Close the file
    '''            
    def close_file(self):
        if self.file != None:
            self.file.close()
            self.file = None
    
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
    
    
    '''
    def try_get_file(self, filename):
        read_data = ""
        filename = path.abspath('cache\\' + filename)
        try:
            with open(filename, "r+") as f:
                read_data = f.read()
            print(read_data)
            return read_data
        except:
            print sys.exc_info()
            print "File not found", filename
            return 0 '''