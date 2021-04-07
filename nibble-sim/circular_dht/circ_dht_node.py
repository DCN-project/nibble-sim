"""
    Implementation of circular distributed hash table.
"""

import logging
import hashlib

from common.node import Node

class CircularDhtNode(Node):

    def __init__(self):
        super().__init__()
        logging.basicConfig(level=logging.INFO)

    def generateHash(self, key):
        """
            Generates hash for the given key using SHA-1 algorithm.

            Parameters
            ----------
            key : str

            Returns
            -------
            hash : str
        """
        return hashlib.sha1(key.encode())

    def startNewNetwork(self, nodeID, portNo):
        """
            Start a new P2P network with user defined nodeID and listens to portNo.

            Parameters
            ----------
            nodeID : str
            portNo : int
        """
        self.nodeID = str(nodeID)
        self.setupNode(portNo)

        # intimate the log server on the addition of node
        self.sendMsg("New network started by node: "+ self.nodeID + ". Listening on port: " + str(portNo), self.LOG_SERVER_PORT)
        logging.info("New network started.")

    def joinNetwork(self, nodeID, portNo):
        """
            Join an existing P2P network through a node on the network.
            The way nodeID and portNo are obtained are upto the user and/or P2P protocol.

            Parameters
            ----------
            nodeID : str
                Identifier of the node in the P2P network through which new node wishes to join.
            portNo : int 
                Port number on which the existing node is listening.
        """
        self.nodeID = str(nodeID)
        self.setupNode(portNo)

        # intimate the log server on the addition of node
        self.sendMsg("New network started by node: "+ self.nodeID + ". Listening on port: " + str(portNo), self.LOG_SERVER_PORT)

        pass

    def sendMsg(self, msg, nodeId):
        """
            Sends message to a nodeID and to LogServer

            Parameters
            ----------
            msg : str
            nodeID : str
        """
        # TODO: Convert nodeID into port number
        port = nodeId

        # TODO: replace self.portNo with self.nodeID
        to_send_msg = " F:" + str(self.portNo) + "T:" + str(nodeId) +"M:" + msg
        
        if port != self.LOG_SERVER_PORT:
            if not self.send(to_send_msg, port):
                logging.warning("Could not send message to port: " + str(port))
                to_send_msg = to_send_msg + " | FAILED"     # modify the message and send it to log server

        if not self.send(to_send_msg, self.LOG_SERVER_PORT):
            logging.warning("Could not send message to log server.")
        
    def processRqst(self, msg):
        logging.info(msg)

    def run(self):
        """
            The main function that enables the user interact with the node and hence then P2P network.
        """
        print('\nDo you want to start a new network[N] or join an existing one [E]?')
        user_choice = input('Your choice [N|E]: ')
        if user_choice == 'N':
            nodeId = input("Enter the node identifier of your choice: ")
            port = input("Enter the port on which the node listens: ")
            try:
                self.startNewNetwork(nodeId, int(port))
            except ValueError:  # if the port number by user is not a valid integer
                print("Invalid port number. Shutting down node...")
        elif user_choice == 'E':
            nodeId = input("Enter the node identifier of an existing node: ")
            port = input("Enter the port on which the existing node listens: ")
            try:
                self.joinNetwork(nodeId, int(port))
            except ValueError:  # if the port number by user is not a valid integer
                print("Invalid port number. Shutting down node...")
        else:
            print('Invalid choice. Shutting down node...')

        print("Instantiated node. Listening on port number: ", self.portNo)
        print("*** Type 'S' to send messages *** ")
        while not self.shutdown:
            try:
                cmd = input('Your choice [S]: ')
                if cmd == 'S':
                    msg = input("Enter the message: ")
                    portNo = input("Enter the target port number: ")
                    self.sendMsg(msg, int(portNo))
                else:
                    print("Invalid choice!")

            except KeyboardInterrupt:
                print("[KEYBOARD INTERRUPT]")
                break