"""
    Implementation of circular distributed hash table.
"""

import logging

from common.node import Node

class CircularDhtNode(Node):

    def __init__(self, portNo):
        super().__init__()
        logging.basicConfig(level=logging.INFO)
        self.setupNode(portNo)

        # intimate the log server on the addition of node
        self.sendMsg("Node added. Port: " + str(portNo), self.LOG_SERVER_PORT)

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

    pass