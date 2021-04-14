import re
import logging
from common.node import Node

# network visualization imports
import networkx as nx
import matplotlib.pyplot as plt
import multiprocessing as mp

"""
    Log server class logging transactions in the P2P network onto a single terminal.
"""

class LogServer(Node):

    def __init__(self):
        super().__init__()
        logging.basicConfig(level=logging.INFO)
        self.setupNode(self.LOG_SERVER_PORT)
        self.showNtwrkViz = False

    def __ntwrkVizSetup(self):
        """
            Setting up for visualizing the network
        """
        self.showNtwrkViz = True
        self.curNtwrk = nx.Graph()
        self.plot_pipe, plotter_pipe = mp.Pipe()
        self.plotter = NtwrkPlotter()
        self.plot_process = mp.Process(
            target=self.plotter, args=(plotter_pipe,), daemon=True)
        self.plot_process.start()
    
    def __plot(self, closePlotter=False):
        """
            Sends commands to the network plotter

            Parameters
            ----------
            closePlotter : bool
                if set true, sends a close command to the network plotter process
        """
        send = self.plot_pipe.send
        if closePlotter:
            send(None)
        else:
            send(self.curNtwrk)

    def startNewNetwork(self, nodePortNo):
        pass

    def joinNetwork(self, existingPortNo, nodePortNo):
        pass
    
    def close(self):
        self.__plot(None)   # end the network plotter process
        super().close()

    def sendMsg(self):
        pass
    
    def processRqst(self, msg):
        logging.info(msg)

        if self.showNtwrkViz:
            # not visualising the request if the message was not sent to the intended receiver
            if re.search(".FAILED.*", msg):
                return
            
            data = re.split(":", msg)

            if data[0] == 'T':
                if data[2] == 'N': # Node starting a new network
                    self.curNtwrk.add_node(data[3])
                    logging.info("Add edge: " + data[3])
                    self.__plot()
                elif data[2] == 'USP': # <UPDATE-SUCCESSOR-PREDECESSOR>
                    self.curNtwrk.add_edge(data[1], data[4])
                    logging.info("Add edge: " + data[1]  + " " + data[4])
                    if data[5] != data[4]:
                        self.curNtwrk.add_edge(data[1], data[5])
                        logging.info("Add edge: " + data[1] + " " + data[5])
                    
                    if (len(self.curNtwrk.adj[data[4]]) > 2) or (len(self.curNtwrk.adj[data[5]]) > 2):
                        print("DEBUG:adj:" + data[4] + ":" + str(len(self.curNtwrk.adj[data[5]])))
                        print("DEBUG:adj:" + data[4] + ":" + str(len(self.curNtwrk.adj[data[5]])))
                        self.curNtwrk.remove_edge(data[4], data[5])
                        logging.info("Remove edge: " + data[4]  + " " + data[5])
                    self.__plot()
                elif data[2] == 'X': # Node leaving the network
                    adjacents = list(self.curNtwrk.adj[data[3]])
                    if len(adjacents) == 2:
                        self.curNtwrk.add_edge(adjacents[0], adjacents[1])
                        logging.info("Add edge: " + adjacents[0]  + " " + adjacents[1])
                    elif len(adjacents) > 2:
                        logging.error("BUG!!!!!!!!!!!!!!!!!!!!!!")
                    self.curNtwrk.remove_node(data[3])
                    logging.info("Remove node: " + data[3])

                    self.__plot()
                
    def run(self):
        print('\nDo you wish to visualize the network ?')
        user_choice = input("Type 'y' for yes: ")
        if user_choice == 'y':
            self.__ntwrkVizSetup()
        else:
            print('Not visualizing the network.')
        while not self.shutdown:
            pass

class NtwrkPlotter:
    """
        Handles network plotting in a background process.
    """
    def __init__(self):
        pass

    def terminate(self):
        plt.close('all')

    def call_back(self):
        while self.pipe.poll():
            command = self.pipe.recv()
            if command is None:
                self.terminate()
                return False
            else:
                self.ax.cla()
                nx.draw(command, ax=self.ax, pos=nx.planar_layout(command), with_labels=True)
        self.fig.canvas.draw()
        return True

    def __call__(self, pipe):
        print('initializing network plotter...')

        self.pipe = pipe
        self.fig, self.ax = plt.subplots()
        timer = self.fig.canvas.new_timer(interval=100)
        timer.add_callback(self.call_back)
        timer.start()

        print('...done')
        plt.show()