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

    def processRqst(self, msg):
        logging.info(msg)