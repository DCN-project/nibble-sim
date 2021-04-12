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

    def startNewNetwork(self, nodePortNo):
        """
            Start a new P2P network with user defined node and listens to nodePortNo.

            Parameters
            ----------
            nodePortNo : int
        """
        self.setupNode(nodePortNo)

        # intimate the log server on the addition of node
        self.sendMsg("New network started by a node listening on port: " + str(nodePortNo), self.LOG_SERVER_PORT)
        logging.info("New network started.")

    def joinNetwork(self, existingPortNo, nodePortNo):
        """
            Join an existing P2P network through a node on the network.

            Parameters
            ----------
            existingPortNo : int
                Port number on which the existing node is listening
            nodePortNo : int 
                Port number on which the node is listening
        """
        self.setupNode(nodePortNo)

        # send <JOIN-NETWORK>
        rpc = "J:" + str(self.portNo)
        if self.sendMsg(rpc, existingPortNo):
            logging.info("Sent <JOIN-NETWORK> to existing port: " + str(existingPortNo) + ". Waiting for reply.")
        else:
            logging.error("Could not send join network request to port: " + str(existingPortNo) + ". Shutting down node...")
            self.close()

        # intimate the log server on the addition of node
        self.sendMsg("Node added. Listening on port: " + str(nodePortNo) , self.LOG_SERVER_PORT)

        pass

    def sendMsg(self, msg, nodeId):
        """
            Sends message to a nodeID and to LogServer

            Parameters
            ----------
            msg : str/int
            nodeId : str (port number of receiver as a string or int)

            Returns
            -------
            success : boolean
                True if message was successfully sent; else False
        """
        port = int(nodeId)

        logMsg = " T:" + str(nodeId) + " " + msg
        
        if port != self.LOG_SERVER_PORT:
            if not self.send(msg, port):
                logging.warning("Could not send message to port: " + str(nodeId))
                logMsg = logMsg + " | FAILED"     # modify the message and send it to log server
                if not self.send(logMsg, self.LOG_SERVER_PORT):
                    logging.warning("Could not send message to log server.")
                return False

        if not self.send(logMsg, self.LOG_SERVER_PORT):
            logging.warning("Could not send message to log server.")

        return True
        
    def processRqst(self, msg):
        logging.info(msg)

    def run(self):
        """
            The main function that enables the user interact with the node and hence then P2P network.
        """
        print('\nDo you want to start a new network[N] or join an existing one [E]?')
        user_choice = input('Your choice [N|E]: ')
        if user_choice == 'N':
            port = input("Enter the port on which the node listens: ")
            try:
                self.startNewNetwork(int(port))
            except ValueError:  # if the port number by user is not a valid integer
                print("Invalid port number. Shutting down node...")
        elif user_choice == 'E':
            existingPort = input("Enter the port on which the existing node listens: ")
            newPort = input("Enter the port on which the node listens: ")
            try:
                self.joinNetwork(int(existingPort), int(newPort))
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