# On simulation for P2P network
This document provides a brief literature review of simulators/simulation for a P2P network.

## Why make a simulator?
- In order to propose, design, implement, and evaluate new P2P technologies, there is a key problem: how can experiments be performed and monitored in a “real” environment? Due to the complexity and scale of real P2P networks, a popular option is to use computer simulations.
- A P2P network can be simulated on one or more computers, allowing for the behavior of peers to be monitored precisely, giving the possibility
for iterative design, and perhaps most importantly, detailed evaluation.

## Classes of P2P simulators
1. Query Cycle Simulation: loops through each node in
the overlay network, and carries out queries for network as and when required.
2. Discrete Event Simulation: maintains a thread scheduler that synchronizes a queue of messages to be transferred between the simulated nodes of the overlay network.

## Requirements from a P2P network simulator
- To simulate a dynamic network requires the ability to acquire bootstrap nodes, such as uniformly at random (random graph), from a distinct set of nodes (supernodes) or possibly a single node (central control). Without such facilities, these will need to be manually designed and implemented.
- It should support modeling of realistic transport
protocols, for example, message queueing.
- While P2P networks are overlay networks, many
a time P2P researchers are interested in testing their protocols with different implementations of the underlying network, for example:
    - Topology generation (random, circular)
    - Network latency and bandwidth including any variation between any pair of nodes and congestion between nodes
    - Different types of access links (Ethernet, WiFi, 3G, LTE)
    - Ability to model a node’s computational capabilities in terms of processing power and storage specified in compute units
- P2P overlay networks often need to model the behavior of individual nodes in terms of features, for example:
    - Misbehavior (intentional or unintentional)
    - Message loss
    - Mobility models, such as the mobile waypoint model
    - Churn with parameterized distribution models
    - Node failure
- The ability to generate statistical data about a simulator run is an essential feature for a P2P simulator. Certain properties of such statistics generation are to be expected, for example:
    - Support for output formats, such as SQL, XML, text
    - Mechanisms for logging experiments
    - Network graph properties, such as HITTS, PageRank, power law, centrality, betweenness
    - Support for GraphML (a versatile graph file format) or similar
- The simulator should:
    - Adhere to standard programming interfaces, such as the Common API when simulating DHTs
    - Provide clear documentation
    - Have user community support through forums or a mailing list, amongst others
    - Have a reference implementation of well-known P2P protocols, for example, Chord, Kad network, CAN, Tapestry, and so on
    - Have a GUI for visualization of various aspects of the simulation

[Back to home](./Home.md)