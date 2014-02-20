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
    classdocs
    '''
    file = None

    def __init__(self, filename):
        self.filepath = "cache/" + self._strip(filename) + '.txt'
        '''
        Constructor
        '''
    
    def try_open_file(self):
        if self.file == None:
            try:
                self.file = open(self.filepath, 'r+')
                return 1
            except:
                self.file = open(self.filepath, 'w+')
                return 0
                
    def close_file(self):
        if self.file != None:
            print("close file.")
            self.file.close()
            self.file = None
    
    def cache_data(self, data):
        #data = data.decode("utf-16")
        #content = unicode(q.data.strip(codecs.BOM_UTF8), 'utf-8')
        if self.file == None:
            raise Exception("Unable to cache, file not found")
        else:
            #print(data)
            self.file.write(data)
            
    def read_cache(self):
        if self.file == None:
            raise Exception("Unable to read cache, file not found")
        else:
            return self.file.readline()
    
    def _strip(self, s):
        #re.sub(r'[\W_]+', '', s)
        s = ''.join(e for e in s if e.isalnum())
        #print("S:", s)
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