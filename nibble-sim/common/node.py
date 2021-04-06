# Importing socket library in python
import socket
import sys
import time
import threading


""" 
    Class with functions to create & handle a node.
"""
class Node:

    # Constructor
    def __init__(self, portNo):
        self.HOST = '127.0.0.1'      # Host (IP Address)
        self.portNo = portNo       # port number
        #self.nodeID = nodeID      # Node ID (lies between 1 to number of nodes in the peer network)
        self.sock = []        # Socket object [serveSocket, clientSocket]
        self.allConn = []     # Holds the objects of all the connections
        self.allAddr = []     # Holds the address of all the connections
        self.prevNode = {}    # Dictionary -> nodeID: [host, portNO]
        self.nextNode = {}    # Dictionary -> nodeID: [host, portNO]
        self.shutdown = False
        self.clientFlag = True

        self.msgFormat = 'utf-8'

        self.__createSocket()
        self.__bindSocket(2)

        # Check Peer status, if there are active nodes in the peer, ping them for joining 
        # the network. If not, you are instantiating a peer network with first active node
        # if self.peerStatus:
        #     print("Please enter the host of an active nodes in peer: ")
        #     activeHost = input()
        #     print("Please enter the port number of the node: ")
        #     activePort = input()

        #     self.connectNode(activeHost, activePort)

        # Creating a thread for server
        self.serverThread = threading.Thread(target=self.__acceptConn)
        self.serverThread.daemon = True
        self.serverThread.start()

    def __createSocket(self):
        '''
            create socket (self)
        ''' 
        try:
            self.sock.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))
            self.sock.append(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

        except socket.error as msg:
            print("[ERROR] Socket creation error: " + str(msg))
    
    def __bindSocket(self, listenNo):
        ''' 
            Bind socket (self, listenNo)
            listenNo ---> Number of connections it will accept 
        '''
        try:
            print("[PORT BINDED] Binding the Port: " + str(self.portNo))
            self.sock[0].bind((self.HOST, self.portNo))
            self.sock[0].listen(listenNo)

        except socket.error as msg:
            print("[ERROR] Socket binding error: " + str(msg))

    def __acceptConn(self):
        '''
            Accept connection from other nodes (self)
            Makes 5 attempts to check and accept a connection
        '''
        for i in self.allConn:
            i.close()

        del self.allConn[:]
        del self.allAddr[:]

        while not self.shutdown:
            try:
                conn, address = self.sock[0].accept()
                self.sock[0].setblocking(1)  # prevents timeout

                self.allConn.append(conn)
                self.allAddr.append(address)

                print("[NEW CONNECTION] Connection has been established to :" + address[0])

                for i in range(len(self.allConn)):
                    data = self.allConn[i].recv(1024)
                    if len(data) > 0:
                        print("[NEW MESSAGE] Message received from Node-", self.allAddr[i], " : ", data)

            except KeyboardInterrupt:
                print("[ERROR] accepting connections. Trying again...")

            except socket.error as msg:
                print("[ERROR] Cannot accept any connections: " + str(msg))

        self.sock[0].close()
        print("Socket closed")
            
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
            self.sock[1].send(msg.encode(self.msgFormat))

            if waitReply:
                print(self.sock[1].recv(1024).decode(self.msgFormat))

        except KeyboardInterrupt:
            print("[ERROR] Keyboard interrupt detected")
        
        except socket.error as msg:
            print("[ERROR] Cannot send message to the target node:", str(msg))
        
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
