import logging
from common.node import Node

"""
    Log server class logging transactions in the P2P network onto a single terminal.
"""

class LogServer(Node):

    def __init__(self):
        super().__init__()
        logging.basicConfig(level=logging.INFO)
        self.setupNode(self.LOG_SERVER_PORT)

    def startNewNetwork(self, nodePortNo):
        pass

    def joinNetwork(self, existingPortNo, nodePortNo):
        pass

    def sendMsg(self):
        pass
    
    def processRqst(self, msg):
        logging.info(msg)
    
    def run(self):
        while not self.shutdown:
            pass