'''
    Main file (To be run in each terminal)
'''

# Importing nodeObject class
from common.node import Node
import sys
import logging
import signal

node = None

def signal_handler(sig, frame):
    print('Closing node...')
    node.close()
    print('Closed node.\nExiting...')
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    print('Welcome to nibble-sim!')
    print('----------------------')
    print('Developed by Vishva Bhate & Mayank Mehta\n')

    portNo = input("Enter port number for the node: ")

    # instantiate the node with the user input port number and logger level
    node = Node(int(portNo), logging.DEBUG)
    
    print("To send a message, type: send")
    print("Press CTRL+C to end the chatbox")
    print("-----------------------------------------------------------------------")
    print("Chatbox begins:")
    print("_______________________________________________________________________")
    
    while True:
        try:
            cmd = input()
            if cmd == 'send':
                msg = input("Enter the message: ")
                portNo = input("Enter the target port number: ")
                node.send(msg, int(portNo))

        except KeyboardInterrupt:
            print("[KEYBOARD INTERRUPT]")
            break