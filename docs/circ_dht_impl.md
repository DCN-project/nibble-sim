# Circular DHT Implementation

> The implementation is an amalgamation of notes presented [here](./circ_dht.md) and the original paper describing Chord DHT.

> All node IDs are written within parenthesis while the keys are written in square-brackets.

> The nibble-sim simulated in it's current state can only be used on a single computer. The capability of using the same software across different physical devices is lacking but it can be easily incorporated in the set framework.

### Hash function
- A consistent hash function is used to assign each node and key an *m*-bit identifier. This hash function is **SHA-1**.
- A node's identifier is chosen by hashing the node's IP address&|/port number, while a key identifier is produced by hashing the key.

### Assigning keys to nodes
- Identifiers are ordered in an identifier circle modulo *2^m*.
- Key (*k*) is assigned to the first node whose identifier is equal to or follows *k* in the identifier space. This node is called the successor node of key *k* - denoted as *succesor(k)*.
- If identifiers are represented as a circle of numbers from *0 to (2^m - 1)*, then *succesor(k)* is the first node clockwise from *k*.
- The following example is taken from MIT's original paper on Chord:
![chord-basic-example](./images/chord_identifier_circle_eg.png)
    - Numbers in bold (0-7) are possible node IDs.
    - Numbers within the rectangle represent a key to be stored.
    - There are only 3 nodes in the network with network IDs (0), (1), (3).
    - Key [1] will be stored in node (1) because the node with the same node ID exists. Node ID (1) is the successor of [1] => *successor([1]) = 1*.
    - Key [2] would have been stored in node 2, but since no node with such ID exists, the key is associated with node ID closest to 2 and existing on the network. Hence, [2] is stored in node 3 => *successor([2]) = 3*.
    - Similar explanation is valid for assignment of key [6]=> *successor([6]) = 0*.

### Routing information at each node
- Each node knows the IP address of it's successor and it's predecessor in the network.
- The above information is stored in the routing table of the node.

### Node joining the network
- For a node to join the network, it sends a *join* request to any existing node's IP address. It is assumed that there exists an external mechanism through which the IP address&|/port number of a node (n') in the network is known to a new joinee, *n*. The following details are sent in the *join* request:
    1. Port number on which *n* listens

    After (n') receives the *join* request, the following steps are executed:
    1. (n') calculates the hash of the IP address&|/port number of *n*.
    2. Compares the hash(n) with the hash of it's own IP address&|/port number:
        ```
        if (hash(n) > hash(n')):
            if (hash(n) < hash(successor(n'))):
                - (n') replies to (n) with <UPDATE-SUCCESSOR-PREDECESSOR>:
                    - IP address&|/port number of (n') as (n)'s predecessor
                    - IP address&|/port number of (n')'s successor ( - n'') as (n)'s successor
                - (n') sends a message to (n'') with IP address&|/port number of (n) as (n'')'s predecessor <UPDATE-PREDECESSOR>
                - (n') updates it's routing table with (n) as it's successor
            else:
                - (n') sends (n'') <FIND-SUCCESSOR>:
                    - IP address&|/port number of (n) and requests (n'') to find successor of (n)
        else (hash(n) < hash(n')):
            if (hash(n) > hash(predecessor(n'))):
                - (n') replies to (n) with <UPDATE-SUCCESSOR-PREDECESSOR>:
                    - IP address&|/port number of (n') as (n)'s successor
                    - IP address&|/port number of (n')'s predecessor ( - 'n) as (n)'s predecessor
                - (n') sends a message to ('n) with IP address&|/port number of (n) as ('n)'s successor <SUCCESSOR-UPDATE>
            else:
                - (n') sends ('n) <FIND-PREDECESSOR>:
                    - IP address&|/port number of (n) and requests ('n) to find predecessor of (n)
        ```
    3. Transferring of keys: (n) can become the successor only for keys that were previously the responsibility of the node immediately following (n). So, (n) only needs to contact that one node to transfer responsibility for all relevant keys. \<TRANSFER-KEY\>

### Node leaving the network
- Whenever a node (n) leaves the network, keys assigned to (n) will be reassigned to it's successor.
- The routing table of it's predecessor is also updated.

### Resolving query
![query_resolve](./images/query_resolve.jpg)
- The IP address of the node initiating the query also flows with the query request.

### Log server (only for simulation)
- To better understand how communication is happening between the peers in the network, a copy of every message that a peer sends to other peer is sent to the **log server**. The log server is just another terminal acting as a server and receiving a copy of messages and displaying them. Additional functionality to store the logs into a file can be added (depends upon time constraints).
- Each peer in the simulation would be a terminal. Hence, message received or sent by the peer would be displayed on the terminal of each peer.

### FAQs
**Q1.** Why should a node (n) store the IP address of its successor in it's routing table?

**A1.** Given that the nodes in circular DHT are arranged in an identifier circle, if node (n) does not store information about its successor, it won't know where to look-up for keys that are not stored in it. The circular network will not be able to form in this case.

**Q2.** Why should a node (n) also store the IP address of its predecessor?

**A2.** Storing predecessor helps in moving messages around the circle in both the directions.

[Back to home](./Home.md)