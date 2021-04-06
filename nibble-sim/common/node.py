# Importing socket library in python
import socket
import sys
import time
import threading
import logging
from abc import ABC, abstractmethod

""" 
    Abstract class with functions to create & handle a node.
"""
class Node(ABC):

    def __init__(self):
        """
           Must be called by every derived class in the beginning as
           super.__init__()
        """
        self.HOST            = '127.0.0.1'      # Constant host IP address
        self.LOG_SERVER_PORT = 31418            # Constant port number of log server
        self.MSG_FORMAT = 'utf-8'               # Constant message format
        self.shutdown = False                   # Flag to indicate node shutdown

    def setupNode(self, portNo):
        """
            Sets the initial values of the attributes. Must be called by every derived class in __init__

            Parameters
            ----------
            portNo : int
                Port number on which the node listens
        """
        self.portNo = portNo                    # port number

        self.sock = []        # Socket object [serverSocket, clientSocket]
        self.clientFlag = True

        self.createSocket()
        if (self.bindSocket(2)):
            # Creating a thread to listen to requests
            self.listener = threading.Thread(target=self.listenRqsts)
            self.listener.daemon = True
            self.listener.start()
        else:
            self.close()

    def createSocket(self):
        '''
            create socket (self)
        ''' 
        try:
            self.sock.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
            self.sock.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

        except socket.error as msg:
            logging.error("Socket creation error: " + str(msg))
    
    def bindSocket(self, listenNo):
        ''' 
            Bind socket (self, listenNo)
            listenNo ---> Number of connections it will accept 

            Returns
            -------
            success : bool
                True if the socket is successfully binded to given port number; else False 
        '''
        try:
            logging.debug("[PORT BINDED] Binding the Port: " + str(self.portNo))
            self.sock[0].bind((self.HOST, self.portNo))
            self.sock[0].listen(listenNo)
            return True

        except socket.error as msg:
            logging.error("[ERROR] Socket binding error: " + str(msg))
            logging.info("Cannot bind to port number: " + str(self.portNo) + " | Exiting node...")
            return False

    def listenRqsts(self):
        '''
            Accept connection from other nodes (self)
            Makes 5 attempts to check and accept a connection
        '''

        allConn = []
        allAddr = []

        while not self.shutdown:
            try:
                conn, address = self.sock[0].accept()
                self.sock[0].setblocking(1)  # prevents timeout

                allConn.append(conn)
                allAddr.append(address)
                
                logging.debug("[NEW CONNECTION] Connection has been established to :" + address[0])

                for i in range(len(allConn)):
                    data = allConn[i].recv(1024)
                    if len(data) > 0:
                        logging.debug("[NEW MESSAGE] Message received from Node-" + str(allAddr[i]) + " : " + str(data)[2:-1])
                        self.processRqst(str(data)[2:-1])

            except KeyboardInterrupt:
                logging.error("[ERROR] accepting connections. Trying again...")

            except socket.error as msg:
                logging.error("[ERROR] Cannot accept any connections: " + str(msg))
                self.close()

        self.sock[0].close()
        logging.debug("Socket closed")

    @abstractmethod
    def processRqst(self, msg):
        """
            Processes the request messages obtained by the node. Should only be called from within
            listenRqsts function. Must be defined by each of the child class.

            Parameters
            ----------
            msg : str
                Message string received by the node.
        """
        pass

    def send(self, msg, port, waitReply=False):
        '''
            Connect to a node and send message.

            Parameters
            ----------
            msg : str
                Message to send
            port : int
                Port number to which message must be sent
            waitReply : bool
                To wait or not to wait for the reply. Default: False
        '''
        try:    
            if not self.clientFlag:
                self.sock[1] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self.sock[1].connect((self.HOST, port))
            self.sock[1].send(msg.encode(self.MSG_FORMAT))

            if waitReply:
                print(self.sock[1].recv(1024).decode(self.MSG_FORMAT))

        except KeyboardInterrupt:
            logging.error("[ERROR] Keyboard interrupt detected")
        
        except socket.error as msg:
            logging.error("[ERROR] Cannot send message to the target node: " + str(msg))
        
        finally:
            self.sock[1].close()
            self.clientFlag = False

    def close(self):
        '''
            Closes all the sockets 
        '''
        self.shutdown = True
        self.sock[0].close()
        if self.clientFlag:
            self.sock[1].close()

if __name__=='__main__':
    print('Abstract class. Cannot run the module.')
    pass