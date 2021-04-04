'''
Main file (To be run in each terminal)
'''

# Importing nodeObject class
import nodeConnection
import sys

if __name__ == '__main__':
    


    host = input("Enter host for the node: ")
    portNo = input("Enter port number for the node: ")

    node = nodeConnection.nodeObject(host, int(portNo))
    
    print("Please enter the message to be sent to the node in the following format")
    print("send(msg, host, port number)")
    print("-----------------------------------------------------------------------")
    print("Chatbox begins:")
    print("_______________________________________________________________________")
    
    while True:
        try:
            cmd = input()
            if cmd == 'send':
                msg = input("Enter the message: ")
                host = input("Enter the target host: ")
                portNo = input("Enter the target port number: ")
                node.ConnAndSend(msg, host, int(portNo))

        except KeyboardInterrupt:
            node.close()
            sys.exit()
            print("[KEYBOARD INTERRUPT] Closing the node")
            break