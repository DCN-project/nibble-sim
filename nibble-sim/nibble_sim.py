'''
    Main file (To be run in each terminal)
'''

# Importing nodeObject class
from common.node import Node
import sys

if __name__ == '__main__':
    print('Welcome to nibble-sim!')
    print('----------------------')
    print('Developed by Vishva Bhate & Mayank Mehta\n')

    portNo = input("Enter port number for the node: ")

    node = Node(int(portNo))
    
    print("Please enter the message to be sent to the node in the following format")
    print("send(msg, port number)")
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
            node.close()
            sys.exit()
            print("[KEYBOARD INTERRUPT] Closing the node")
            break