"""
    Abstract class defining the structure for a node in P2P network.
"""

from abc import ABC, abstractmethod

class Node(ABC):

    @abstractmethod
    def store(self, key, value):
        pass

    @abstractmethod
    def findNode(self, nodeID):
        pass

    @abstractmethod
    def findValue(self, key):
        pass

    @abstractmethod
    def sendValue(self, ipAddr, port, value):
        pass

    @abstractmethod
    def ping(self, nodeID):
        pass

    @abstractmethod
    def pingReply(self):
        pass
    
    @abstractmethod
    def generateHash(self, key):
        pass
    
    @abstractmethod
    def getIpAddr(self, nodeID):
        pass

    @abstractmethod
    def joinNetwork(self, ipAddr, port):
        pass

    @abstractmethod
    def leaveNetwork(self):
        pass

    def parseIncomingRequests(self):
        pass

    def log(self, value):
        pass

if __name__=='__main__':
    print('Abstract class. Cannot run the module.')
    pass