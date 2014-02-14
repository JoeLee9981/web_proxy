from client import *

def main():
    c = client('localhost', 12333)
    c.start()

if __name__ == '__main__':
    main()
