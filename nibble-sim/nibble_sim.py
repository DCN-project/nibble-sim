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
        node.run()
    elif node_type == 'P':  # running a peer
        node = CircularDhtNode()
        node.run()
    else:
        print('Invalid node choice! Exiting nibble-sim...')
        
    print('\nSayonara!!!\n')