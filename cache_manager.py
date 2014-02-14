'''
Created on Jan 24, 2014

@author: god_laptop
'''
from os import path
import sys

class cache_manager(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def cache(self, filename, data):
        pass
    
    def try_get_file(self, filename):
        read_data = ""
        filename = path.abspath('cache\\' + filename)
        try:
            with open(filename, "r+") as f:
                read_data = f.read()
            print(read_data)
            return read_data
        except:
            #print sys.exc_info()
            #print "File not found", filename
            return 0 