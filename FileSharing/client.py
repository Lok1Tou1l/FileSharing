from xmlrpc.client import ServerProxy, Fault
from cmd import Cmd
from random import choice
from string import ascii_lowercase 
from server import Node, UNHANDLED
from threading import Thread
from time import sleep
import sys

HEAD_START = 0.1 # Seconds
SECRET_LENGTH = 100

def random_string(length):
    """
    Returns a random string of letters with the given length
    """
    chars =[] 
    letters = ascii_lowercase[:26]
    while length > 0:
        length -=1 
        chars.append(choice(letters))
    return ''.join(chars)

class Client(Cmd):
    prompt = '> '

    def __init__(self,url,directory,urlfile):
        """
        sets the url ,dir name and urlfile , 
        and starts the node server in a different thread 
        """
        Cmd.__init__(self)
        self.secret = random_string(SECRET_LENGTH)
        n = Node(url,directory,self.secret)
        t = Thread(target=n._start)
        t.setDaemon(1)
        t.start()
        # Give the server a head start:
        sleep(HEAD_START)
        self.server = ServerProxy(url)
        for line in open(urlfile):
            line = line.strip()
            self.server.hello(line)
        
    
    def do_fetch(self,arg):
        "Call the fetch method from the server"
        try :
            self.server.fetch(arg,self.secret)
        except Fault as f :
            if f.faultCode != UNHANDLED: raise 
            print("Couldn't find the file",arg)
    
    def do_exit(self,arg):
        "Exit the proogram"
        print()
        sys.exit()
    
    do_EOF = do_exit # EOF is an alias for exit

    def main():
        urlfile,directory,url = sys.argv[1:]
        client = Client(url,directory,urlfile)
        client.cmdloop()
    
    if __name__ == '__main__':
        main()

