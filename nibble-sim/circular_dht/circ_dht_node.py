"""
    Implementation of circular distributed hash table.
"""

import logging
import hashlib

from common.node import Node

class CircularDhtNode(Node):

    def __init__(self, portNo):
        super().__init__()
        logging.basicConfig(level=logging.INFO)
        self.setupNode(portNo)

        # intimate the log server on the addition of node
        self.sendMsg("Node added. Port: " + str(portNo), self.LOG_SERVER_PORT)

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