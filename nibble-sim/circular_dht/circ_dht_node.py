"""
    Implementation of circular distributed hash table.
"""

import logging
import hashlib
import re

from common.node import Node

class CircularDhtNode(Node):

    def __init__(self):
        super().__init__()
        logging.basicConfig(level=logging.INFO)
    
    def setupNode(self, nodePortNo):
        super().setupNode(nodePortNo)
        self.myHash = self.generateHash(str(self.portNo)).hexdigest()
        self.neighbors = [self.portNo, self.portNo]     # 0 -> predecessor | 1 -> successor
        self.hashTable = {}   # Node's own hastable
        self.keyList = {}     # List of all the keys in the network (portNo: [keys])
        self.sharedFolder = {} # List of all shared files
        self.successorHash = self.myHash
        self.predecessorHash = self.myHash
        self.hashTable = {} 

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
        return hashlib.sha1(str(key).encode())

    def startNewNetwork(self, nodePortNo):
        """
            Start a new P2P network with user defined node and listens to nodePortNo.
            
            Parameters
            ----------
            nodePortNo : int
        """
        self.setupNode(nodePortNo)

        # intimate the log server on the addition of node
        self.sendMsg("N:" + str(nodePortNo) + ":New network started by a node", self.LOG_SERVER_PORT)
        logging.info("New network started.")

    def joinNetwork(self, existingPortNo, nodePortNo):
        """
            Join an existing P2P network through a node on the network.
            
            Parameters
            ----------
            existingPortNo : int
                Port number on which the existing node is listening
            nodePortNo : int 
                Port number on which the node is listening
        """
        self.setupNode(nodePortNo)

        # send <JOIN-NETWORK>
        rpc = "J:" + str(self.portNo) + ":" + str(self.portNo)
        if self.sendMsg(rpc, existingPortNo):
            logging.info("Sent <JOIN-NETWORK> to existing port: " + str(existingPortNo) + ". Waiting for reply.")
        else:
            logging.error("Could not send join network request to port: " + str(existingPortNo) + ". Shutting down node...")
            self.close()

        # intimate the log server on the addition of node
        self.sendMsg("Node added. Listening on port: " + str(nodePortNo) , self.LOG_SERVER_PORT)

        pass

    def close(self):
        """
            Send US, UP to node's predecessor and succesor and then closes the node.
        """
        # transfer the keys
        keyRxPortNo = None
        if self.successorHash < self.myHash: # indicating circular overflow
            keyRxPortNo = self.neighbors[0]
        else:
            keyRxPortNo = self.neighbors[1]

        if keyRxPortNo != self.portNo:
            keysToSend = []
            for key in self.hashTable:
                keysToSend.append(key)
            for key in keysToSend:
                if self.sendMsg("SV:" + str(self.portNo) + ":" + key + ":" + str(self.__getValue(key, self.hashTable, True)) + ":ST", keyRxPortNo):
                    logging.info("Transferred key: " + key + " to : " + str(keyRxPortNo))
                else:
                    logging.warning("Could not send <STORE-KEY-VALUE>. Anyways, node is closing.")
        else:
            logging.info("Not transferring keys because I am the single node in the network.")

        if (self.neighbors[0] != self.portNo) and (self.neighbors[1] != self.portNo):
            # send US to predecessor
            rpc = "US:" + str(self.portNo) + ":" + str(self.neighbors[1])
            if not self.sendMsg(rpc, self.neighbors[0]):
                logging.error("Could not send US to predecessor! Anyways leaving the network.")

            # send UP to successor
            rpc = "UP:" + str(self.portNo) + ":" + str(self.neighbors[0])
            if not self.sendMsg(rpc, self.neighbors[1]):
                logging.error("Could not send UP to successor! Anyways leaving the network.")

        if not self.sendMsg("X:" + str(self.portNo), self.LOG_SERVER_PORT):
                logging.error("Could inform log-server about node closure")

        super().close()

    def sendMsg(self, msg, nodeId):
        """
            Sends message to a nodeID and to LogServer
            Parameters
            ----------
            msg : str/int
            nodeId : str (port number of receiver as a string or int)
            
            Returns
            -------
            success : boolean
                True if message was successfully sent; else False
        """
        port = int(nodeId)

        logMsg = "T:" + str(nodeId) + ":" + msg
        
        if port != self.LOG_SERVER_PORT:
            if not self.send(msg, port):
                logging.warning("Could not send message to port: " + str(nodeId))
                logMsg = logMsg + " | FAILED"     # modify the message and send it to log server
                if not self.send(logMsg, self.LOG_SERVER_PORT):
                    logging.warning("Could not send message to log server.")
                return False

        if not self.send(logMsg, self.LOG_SERVER_PORT):
            logging.warning("Could not send message to log server.")

        return True

    def processRqst(self, msg):
        data = re.split(":", msg)
        
        if data[0] == 'J':  # <JOIN-NETWORK>
            if len(data) != 3:
                self.sendMsg("!:" + str(self.portNo), self.LOG_SERVER_PORT)
                logging.warning("Received invalid RPC! msg: " + msg)
                return
            newJoineeHash = self.generateHash(data[2]).hexdigest()

            if (newJoineeHash > self.myHash):
                if (newJoineeHash < self.successorHash) or (self.myHash > self.successorHash):
                    rpc = "USP:" + str(self.portNo) + ":" + str(self.neighbors[1]) + ":" + str(self.portNo)
                    if self.sendMsg(rpc, data[2]):
                        rpc = "UP:" + str(self.portNo) + ":" + str(data[2])
                        if self.sendMsg(rpc, self.neighbors[1]):
                            self.neighbors[1] = int(data[2])
                            self.successorHash = self.generateHash(self.neighbors[1]).hexdigest()
                            logging.info("Updated successor!")
                        else:
                            logging.error("Could not send UP to successor! Old successor retained.")
                    else:
                        logging.error("Could not send USP to new joinee!")
                elif self.neighbors[1] == self.portNo:
                    rpc = "USP:" + str(self.portNo) + ":" + str(self.portNo) + ":" + str(self.portNo)
                    if self.sendMsg(rpc, data[2]):
                        self.neighbors[1] = int(data[2])
                        self.successorHash = self.generateHash(self.neighbors[1]).hexdigest()
                        logging.info("Updated successor!")
                        if self.neighbors[0] == self.portNo:
                            self.neighbors[0] = int(data[2])
                            self.predecessorHash = self.generateHash(self.neighbors[0]).hexdigest()
                            logging.info("Updated predecessor!")
                    else:
                        logging.error("Could not send USP to new joinee!")
                else:
                    rpc = data[0] + ":" + str(self.portNo) + ":" + data[2]
                    if self.sendMsg(rpc, self.neighbors[1]):
                        logging.info("Forwarded J RPC to successor: " + str(self.neighbors[1]))
                    else:
                        logging.error("Could not send J RPC to successor!.")
            else:
                if (newJoineeHash > self.predecessorHash) or (self.predecessorHash > self.myHash):
                    rpc = "USP:" + str(self.portNo) + ":" + str(self.portNo) + ":" + str(self.neighbors[0])
                    if self.sendMsg(rpc, data[2]):
                        rpc = "US:" + str(self.portNo) + ":" + str(data[2])
                        if self.sendMsg(rpc, self.neighbors[0]):
                            self.neighbors[0] = int(data[2])
                            self.predecessorHash = self.generateHash(self.neighbors[0]).hexdigest()
                            logging.info("Updated predecessor!")
                        else:
                            logging.error("Could not send US to predecessor! Old predecessor retained.")
                    else:
                        logging.error("Could not send USP to new joinee!")
                elif self.neighbors[0] == self.portNo:
                    rpc = "USP:" + str(self.portNo) + ":" + str(self.portNo) + ":" + str(self.portNo)
                    if self.sendMsg(rpc, data[2]):
                        self.neighbors[0] = int(data[2])
                        self.predecessorHash = self.generateHash(self.neighbors[0]).hexdigest()
                        logging.info("Updated predecessor!")
                        if self.neighbors[1] == self.portNo:
                            self.neighbors[1] = int(data[2])
                            self.successorHash = self.generateHash(self.neighbors[1]).hexdigest()
                            logging.info("Updated successor!")
                    else:
                        logging.error("Could not send USP to new joinee!")
                else:
                    rpc = data[0] + ":" + str(self.portNo) + ":" + data[2]
                    if self.sendMsg(rpc, self.neighbors[0]):
                        logging.info("Forwarded J RPC to predecessor: " + str(self.neighbors[0]))
                    else:
                        logging.error("Could not send J RPC to predecessor!.")
        
        elif data[0] == 'USP': # <UPDATE-SUCCESSOR-PREDECESSOR>
            if len(data) != 4:
                self.sendMsg("!:" + str(self.portNo), self.LOG_SERVER_PORT)
                logging.warning("Received invalid RPC! msg: " + msg)
                return
            self.neighbors[0] = int(data[3])
            self.neighbors[1] = int(data[2])
            self.successorHash = self.generateHash(self.neighbors[1]).hexdigest()
            self.predecessorHash = self.generateHash(self.neighbors[0]).hexdigest()
            logging.info("Updated successor and predecessor!")

            # sending <TRANSFER-KEYS> to successor
            if self.sendMsg("T:"+str(self.portNo), self.neighbors[1]):
                logging.info("Sent <TRANSFER-KEYS> request to successor")
            else:
                logging.warning("Some problem in sending <TRANSFER-KEYS>")
        
        elif data[0] == 'UP': # <UPDATE-PREDECESSOR>
            if len(data) != 3:
                self.sendMsg("!:" + str(self.portNo), self.LOG_SERVER_PORT)
                logging.warning("Received invalid RPC! msg: " + msg)
                return
            self.neighbors[0] = int(data[2])
            self.predecessorHash = self.generateHash(self.neighbors[0]).hexdigest()
            logging.info("Updated predecessor!")

        elif data[0] == 'US': # <UPDATE-SUCCESSOR>
            if len(data) != 3:
                self.sendMsg("!:" + str(self.portNo), self.LOG_SERVER_PORT)
                logging.warning("Received invalid RPC! msg: " + msg)
                return
            self.neighbors[1] = int(data[2])
            self.successorHash = self.generateHash(self.neighbors[1]).hexdigest()
            logging.info("Updated successor!")
        
        elif data[0] == 'SK': # <STORE-KEY>
            if len(data) != 4:
                self.sendMsg("!:" + str(self.portNo), self.LOG_SERVER_PORT)
                logging.warning("Received invalid RPC! msg: " + msg)
                return
            print(data)
            self.__storeKey(data[2], data[3])
        
        elif data[0] == 'G': # <GET-VALUE>
            if len(data) != 4:
                self.sendMsg("!:" + str(self.portNo), self.LOG_SERVER_PORT)
                logging.warning("Received invalid RPC! msg: " + msg)
                return
            
            if data[3] == "D":
                self.sendMsg("SV:" + str(self.portNo) + ":" + data[2] + ":" + str(self.__getValue(data[2], self.hashTable, True)) + ":ST", int(data[1]))
            elif data[3] == "ND":
                self.sendMsg("SV:" + str(self.portNo) + ":" + data[2] + ":" + str(self.__getValue(data[2], self.hashTable, False)) + ":SH", int(data[1]))
        
        elif data[0] == 'SV': # <STORE-KEY-VALUE>
            if len(data) != 5:
                self.sendMsg("!:" + str(self.portNo), self.LOG_SERVER_PORT)
                logging.warning("Received invalid RPC! msg: " + msg)
                return
            
            if data[4] == "ST":
                self.hashTable.update({data[2]: data[3]})
            elif data[4] == "SH":
                self.sharedFolder.update({data[2]: data[3]})
                print("******************")
                print("SHARED FILE NAME & CONTENT: ", self.sharedFolder)
                print("******************")
                self.sharedFolder = {}

            logging.info("Data stored in node: "+ str(self.portNo))
        
        elif data[0] == 'SHW': # <SHOW-KEYS>
            if len(data) != 2:
                self.sendMsg("!:" + str(self.portNo), self.LOG_SERVER_PORT)
                logging.warning("Received invalid RPC! msg: " + msg)
                return
            
            keyString = str([keys for keys,_ in self.hashTable.items()])
            
            # Pinging the sucessor
            if int(data[1]) != self.neighbors[1]:
                if len(self.hashTable) > 0:
                    self.sendMsg("KR:" + str(self.portNo) + ":" + keyString + ":" + "NP" , int(data[1]))
                self.sendMsg("SHW:" + str(data[1]), self.neighbors[1])

            else:
                if len(self.hashTable) > 0:
                    self.sendMsg("KR:" + str(self.portNo) + ":" + keyString + ":" + "PNE", int(data[1]))
                else: 
                    self.sendMsg("KR:" + str(self.portNo) + ":" + keyString + ":" + "PE", int(data[1]))


        elif data[0] == 'KR': # <KEYS-RECEIVED>
            if len(data) != 4:
                self.sendMsg("!:" + str(self.portNo), self.LOG_SERVER_PORT)
                logging.warning("Received invalid RPC! msg: " + msg)
                return
            
            if data[3] == 'NP' or data[3] == 'PNE':
                keylist = data[2].strip("']['").split("', '")

                for i in keylist:
                    self.keyList.update({i:int(data[1])})

            if data[3] == "PNE" or data[3] == "PE":
                self.__printKeys()

        elif data[0] == 'T': # <TRANSFER-KEYS>
            if len(data) != 2:
                self.sendMsg("!:" + str(self.portNo), self.LOG_SERVER_PORT)
                logging.warning("Received invalid RPC! msg: " + msg)
                return
            rqsterHash = self.generateHash(data[1]).hexdigest()
            keysToSend = []
            for key in self.hashTable:
                if (self.generateHash(key).hexdigest() >= rqsterHash):
                    keysToSend.append(key)
            for key in keysToSend:
                if self.sendMsg("SV:" + str(self.portNo) + ":" + str(key) + ":" + str(self.__getValue(key, self.hashTable, True)) + ":ST", int(data[1])):
                    logging.info("Transferred key: " + key + " to: " + str(data[1]))
                else:
                    logging.warning("Could not send <STORE-KEY-VALUE> to the requester")

        else:
            self.sendMsg("!:" + str(self.portNo), self.LOG_SERVER_PORT)
            logging.warning("Received invalid RPC! msg: " + msg)

        logging.info(msg)

    def run(self):
        """
            The main function that enables the user interact with the node and hence then P2P network.
        """
        print('\nDo you want to start a new network[n] or join an existing one [e]?')
        user_choice = input('Your choice [n|e]: ')
        if user_choice == 'n':
            port = input("Enter the port on which the node listens: ")
            try:
                self.startNewNetwork(int(port))
            except ValueError:  # if the port number by user is not a valid integer
                print("Invalid port number. Shutting down node...")
        elif user_choice == 'e':
            existingPort = input("Enter the port on which the existing node listens: ")
            newPort = input("Enter the port on which the node listens: ")
            try:
                self.joinNetwork(int(existingPort), int(newPort))
            except ValueError:  # if the port number by user is not a valid integer
                print("Invalid port number. Shutting down node...")
        else:
            print('Invalid choice. Shutting down node...')

        print("Instantiated node. Listening on port number: ", self.portNo)
        print("*** Type 'h' for help *** ")
        while not self.shutdown:
            try:
                cmd = input()
                if cmd == 'send':
                    msg = input("Enter the message: ")
                    portNo = input("Enter the target port number: ")
                    self.sendMsg(msg, int(portNo))

                elif cmd == 'store':
                    key = input("Enter the key: ")
                    listLen = input("Enter the length of the value list: ")
                    value = []
                    
                    try:
                        for i in range(int(listLen)):
                            print("Enter element-", i,": ")
                            value.append(input())
                        self.hashTable.update({key: value})
                        self.__storeKey(self.portNo, key)
                    except ValueError: # if the entry by the user is not a valid number
                        print("Invalid length of list. Storing terminated")
                
                elif cmd == 'show':
                    print("******************")
                    print("Compiling a list of files in the network. Please wait...")

                    # Pinging the sucessor
                    if self.portNo != self.neighbors[1]:
                        self.sendMsg("SHW:" + str(self.portNo), self.neighbors[1])
                    else:
                        self.keyList = []
                        self.__printKeys()
                
                elif cmd == 'gd':
                    if not self.keyList:
                        print("There maybe no files in the network. Please execute SHOW command")
                    else:
                        keySel = input("Enter the file name which you wish to get: ")
                        self.sendMsg("G:" + str(self.portNo) + ":" + str(keySel) + ":ND", int(self.__getValue(keySel, self.keyList)))

                    
                elif cmd == 'a':
                    self.__printAboutNode()

                elif cmd == 'h':
                    self.__printHelp()

                else:
                    print("Invalid choice!")

            except KeyboardInterrupt:
                print("[KEYBOARD INTERRUPT]")
                break          



    def __printKeys(self):
        print("******************")
        if not self.hashTable:
            print("No files present on your system")
            print("******************")
        else:
            ctr = 0
            print("Files you present on your system: ")
            for keys,_ in self.hashTable.items():
                ctr += 1
                print(str(ctr) + ".", keys)
            print("******************")

        if not self.keyList:
            print("No files present in the network")
            print("******************")
        else:
            ctr = 0
            print("Files present in the network: ")
            for key,_ in self.keyList.items():
                ctr += 1
                print(str(ctr) + ".", key)
            print("******************")



    def __printHelp(self):
        """
            Prints help
        """
        print("********")
        print("Press 'ENTER' after typing any of the following")
        print("send - send messages")
        print("store - store new file/data")
        print("show - show the list of list of all keys in the network")
        print("gd - Data retreival from neighboring nodes")
        print("a - learn about the node")
        print("h - show this menu")
        print("CTRL+C - shutdown node")
        print("********")


    def __printAboutNode(self):
        """
            Prints information about the node.
        """
        print("********")
        print("Listening port number: ", str(self.portNo))
        print("Predecessor listening port number: ", str(self.neighbors[0]))
        print("Successor listening port number: ", str(self.neighbors[1]))
        if not self.hashTable:
            print("No data stored as of now")
        else:
            print("Data stored: ", self.hashTable)
        print("********")


    def __storeKey(self, lportNo, key):
        """
        Implements the STORE-KEY Function
            - lportNo: lportNo-node-wanting-to-store
            - key: key to be stored
        """
        keyHash = self.generateHash(key).hexdigest()
        rpc = "SK:" + str(self.portNo) + ":" + str(lportNo) + ":" + str(key)
            
        if (keyHash <= self.predecessorHash) and (self.myHash > self.predecessorHash):
            self.sendMsg(rpc, self.neighbors[0])
            logging.info("Finding node for the key at predecessor node: " + str(self.neighbors[0]))

        elif (keyHash > self.myHash) and (self.successorHash > self.myHash):
            self.sendMsg(rpc, self.neighbors[1])
            logging.info("Finding node for the key at successor node: " + str(self.neighbors[1]))

        else:
            if int(lportNo) != self.portNo:
                self.sendMsg("G:" + str(self.portNo) + ":" + str(key) + ":D", int(lportNo))
                return
            logging.info("Data stored in node: " + str(self.portNo))


    def __getValue(self, keyFind, dictionary, delPair=False):
        """
        Used to find values of a key in node's hashtable
            - keyFind: Key whose values are to be sent and deleted
            - dictionary
            - delPair: When True, deletes the (key, value) pair from node's
                       hash-table
        """
        for key, value in dictionary.items():
            if key == keyFind:
                val = value
                if delPair:
                    self.hashTable.pop(key)
                return val
