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

    def processRqst(self, msg):
        logging.info(msg)

    pass