"""
    Implementation of circular distributed hash table.
"""

import logging
import hashlib
import re

from common.node import Node

class CircularDhtNode(Node):

    def __init__(self):
        super().__init__()
        logging.basicConfig(level=logging.INFO)

        self.neighbors = [None, None]     # list of size 2. 0 -> predecessor | 1 -> successor

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
        self.myHash = self.generateHash(str(self.portNo))

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
        self.myHash = self.generateHash(str(self.portNo))

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

    def __printHelp(self):
        """
            Prints help
        """
        print("****\n****")
        print("s - send messages")
        print("a - learn about the node")
        print("h - show this menu")
        print("CTRL+C - shutdown node")
        print("****\n****")

    def __printAboutNode(self):
        """
            Prints information about the node.
        """
        print("****\n****")
        print("Listening port number: ", str(self.portNo))
        print("Predecessor listening port number: ", str(self.neighbors[0]))
        print("Successor listening port number: ", str(self.neighbors[1]))
        print("Data stored (TODO)...")
        print("****\n****")

    def processRqst(self, msg):
        data = re.split(":", msg)

        if data[0] == 'J':  # <JOIN-NETWORK>
            if len(data) != 2:
                self.sendMsg("!:" + str(self.portNo), self.LOG_SERVER_PORT)
                logging.warning("Received invalid RPC!")
                return
            newJoineeHash = self.generateHash(data[1]).hexdigest()
            
            if (newJoineeHash > self.myHash.hexdigest()):
                if self.neighbors[1] is not None:
                    if (newJoineeHash < self.generateHash(self.neighbors[1]).hexdigest()):
                        rpc = "USP:" + str(self.portNo) + ":" + str(self.neighbors[1]) + ":" + str(self.portNo)
                        if self.sendMsg(rpc, data[1]):
                            rpc = "UP:" + str(self.portNo) + ":" + str(data[1])
                            if self.sendMsg(rpc, self.neighbors[1]):
                                self.neighbors[1] = int(data[1])
                                logging.info("Updated successor!")
                            else:
                                logging.error("Could not send UP to successor! Old successor retained.")
                        else:
                            logging.error("Could not send USP to new joinee!")
                    else:
                        if self.sendMsg(msg, self.neighbors[1]):
                            logging.info("Forwarded J RPC to successor: " + str(self.neighbors[1]))
                        else:
                            logging.error("Could not send J RPC to successor!.")
                else:
                    rpc = "USP:" + str(self.portNo) + ":None:" + str(self.portNo)
                    if self.sendMsg(rpc, data[1]):
                        self.neighbors[1] = int(data[1])
                        logging.info("Updated successor!")
                    else:
                        logging.error("Could not send USP to new joinee!")
            else:
                if self.neighbors[0] is not None:
                    if (newJoineeHash > self.generateHash(self.neighbors[0])):
                        rpc = "USP:" + str(self.portNo) + ":" + str(self.portNo) + ":" + str(self.neighbors[0])
                        if self.sendMsg(rpc, data[1]):
                            rpc = "US:" + str(self.portNo) + ":" + str(data[1])
                            if self.sendMsg(rpc, self.neighbors[0]):
                                self.neighbors[0] = int(data[1])
                                logging.info("Updated predecessor!")
                            else:
                                logging.error("Could not send US to predecessor! Old predecessor retained.")
                        else:
                            logging.error("Could not send USP to new joinee!")
                    else:
                        if self.sendMsg(msg, self.neighbors[0]):
                            logging.info("Forwarded J RPC to predecessor: " + str(self.neighbors[0]))
                        else:
                            logging.error("Could not send J RPC to predecessor!.")
                else:
                    rpc = "USP:" + str(self.portNo) + ":" + str(self.portNo) + ":None"
                    if self.sendMsg(rpc, data[1]):
                        self.neighbors[0] = int(data[1])
                        logging.info("Updated predecessor!")
                    else:
                        logging.error("Could not send USP to new joinee!")
            

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
        print("*** Type 'h' for help *** ")
        while not self.shutdown:
            try:
                cmd = input()
                if cmd == 's':
                    msg = input("Enter the message: ")
                    portNo = input("Enter the target port number: ")
                    self.sendMsg(msg, int(portNo))
                elif cmd == 'a':
                    self.__printAboutNode()
                elif cmd == 'h':
                    self.__printHelp()
                else:
                    print("Invalid choice!")

            except KeyboardInterrupt:
                print("[KEYBOARD INTERRUPT]")
                break