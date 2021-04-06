'''
    Main file (To be run in each terminal)
'''

# Importing nodeObject class
from common.log_server import LogServer
from circular_dht.circ_dht_node import CircularDhtNode
import sys
import logging
import signal

node = None

def signal_handler(sig, frame):
    print('Closing node...')
    node.close()
    print('Closed node.\nExiting...')
    print('\nSayonara!!!\n')
    sys.exit(0)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    
    print('Welcome to nibble-sim!')
    print('----------------------')
    print('Developed by Vishva Bhate & Mayank Mehta')
    print('----------------------')
    print("Press CTRL+C to exit nibble-sim\n")

    print("Enter the type of node:\n1) Log Server [L]\n2) Peer [P]")
    node_type = input("Your choice [L|P]: ")
    
    if node_type == 'L':    # running log server
        print("Displaying the logs...")
        node = LogServer()
        while not node.shutdown:
            pass
    elif node_type == 'P':  # running a peer
        portNo = input("Port number: ")
        node = CircularDhtNode(int(portNo))
        print("Instantiated node. Listening on port number: ", portNo)
        print("*** Type 'S' to send messages *** ")
        while not node.shutdown:
            try:
                cmd = input('Your choice [S]: ')
                if cmd == 'S':
                    msg = input("Enter the message: ")
                    portNo = input("Enter the target port number: ")
                    node.send(msg, int(portNo))
                else:
                    print("Invalid choice!")

            except KeyboardInterrupt:
                print("[KEYBOARD INTERRUPT]")
                break
    else:
        print('Invalid node choice! Exiting nibble-sim...')
        
    print('\nSayonara!!!\n')