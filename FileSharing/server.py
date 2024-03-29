from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.client import ServerProxy, Fault
from os.path import join,isfile,abspath
from urllib.parse import urlparse
import sys 

SimpleXMLRPCServer.allow_reuse_address = 1

MAX_HISTORY_LENGTH = 6

UNHANDLED = 100
ACCESS_DENIED = 200

class UnhandledQuery(Fault):
    """
    An exception that represents an unhandled query.
    """
    def __init__(self,message="couldn't handle the query"):
        super().__init__(UNHANDLED,message)
    
class AccessDenied(Fault):
    """
    An Exception that is raised if a user try to access a ressource without permission
    """
    def __init__(self,message="Access denied"):
        super().init__(ACCESS_DENIED,message)

def inside(dir,name):
    """
    Check if a file is inside a directory
    """
    dir = abspath(dir)
    name = abspath(name)
    return name.startswith(join(dir,''))

def get_port(url):
    """
    Extract the port from an URL
    """
    name = urlparse(url)[1]
    parts = name.split(':')
    return int(parts[-1])

class Node:
    """
    A node in a peer-to-peer network
    """
    def __init__(self,url,dirname,secret):
        self.url = url
        self.dirname = dirname 
        self.secret = secret
        self.known = set()
    
    def query(self,query,history=[]):
        """
        Performs a query for a file , possibly asking other known Nodes for help. Returns the file as a string.
        """
        try:
            return self._handle(query)
        except UnhandledQuery:
            history = history + [self.url]
            if len(history) >= MAX_HISTORY_LENGTH:
                raise 
            return self._broadcast(query,history)

    def hello(self,other):
        """
        Used to introduce the Node to other nodes 
        """
        self.known.add(other)
        return 0
    
    def fetch(self,query,secret):
        """
        Used to make the node find a file and download it
        """
        if secret !=  self.secret:
            raise AccessDenied 
        result = self.query(query)
        f = open(join(self.dirname,query))
        f.write(result)
        f.close()
        return 0 
    
    def _start(self):
        """
        Used internally to start the XML-RPC server
        """
        s = SimpleXMLRPCServer(("",get_port(self.url)),logRequests=False)
        s.register_instance(self)
        s.serve_forever()
    
    def _handle(self,query):
        """
        Used internally to handle queries
        """
        dir = self.dirname
        name = join(dir,query)
        if not isfile(name): raise UnhandledQuery
        if not inside(dir,name): raise AccessDenied 
        return open(name).read()
    
    def _broadcast(self,query,history):
        """
        Used internally to broadcast a query to all known Nodes
        """
        for other in self.known.copy():
            if other in history: continue
            try :
                s = ServerProxy(other)
                return s.query(query,history)
            except Fault as f :
                self.known.remove(other)
            raise UnhandledQuery
    
    def main():
        url,directory,secret = sys.argv[1:]
        n = Node(url,directory,secret)
        n._start()


