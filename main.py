'''
Due on Jan 25, 2014
CS4480-001
@author: Joseph Lee

Main Method
'''
import sys

from proxy_server import proxy_server

def main(argv):
    if(len(argv) != 1):
        print("Invalid Command Line Arguments")
    else:
        try:
            port = int(argv[0])
            s = proxy_server("localhost", port)
            s.start()
        #except:
            #print("Unexpeced Exception encountered")
        finally:
            s.close()
            print("Closing Server")

if __name__ == '__main__':
    main(sys.argv[1:])