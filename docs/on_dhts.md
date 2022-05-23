# On Distributed Hash Tables

> A distributed hash table or DHT is a data structure to store data and routing information across a cluster of nodes without a centralized server.

## Why is this needed?
Imagine you are on a network and you want to access the value of a key. There is no centralized server. One naive way to go about searching for the key is to start pinging the nodes closer to you. If they have it, you get your value. If they do not have it, then you ask them to ping other nodes and this continues till you get the location where your key is stored and hence get access to the value. This process is called **flooding**. 
### Problems with flooding
- Key lookup becomes linear
- System is less deterministic and lends itself to cycles, increasing code complexity to do correctly

Hence, we need a more efficient solution to this problem.

## So what DHT does?
- Consider a P2P network for file sharing. A typical hash table would look something like this

	| File name (key) | File location (value) | Node Name |
	| --- | --- | --- |
	| A_gentle_intro_to_ros.pdf | 152.19.10.4 | Alice |
	| Analog-to-digital-comm.pdf | 172.18.1.234 | Bob |
	| Data-comm-nets.pdf | 189.68.0.29 | Charlie |
	| Signals-and-systems.pdf | 232.15.98.134 | Dave |

- Let's say Alice wants to download file named "Data-comm-nets.pdf". She would need to figure out at what IP address is the file located. If she would have the above table with her, she can easily ping Charlie and get the file. 
- We could also use a hash function to generate keys instead of directly using the string names. This step would make the aforementioned table into a hash table like this

	| Hash key | File location (value) | Node Name |
	| --- | --- | --- |
	| 15642 | 152.19.10.4 | Alice |
	| 64795 | 172.18.1.234 | Bob |
	| 31456 | 189.68.0.29 | Charlie |
	| 34975 | 232.15.98.134 | Dave |
- But imagine, if instead of 4, there were 4^6 nodes in the network. Is it feasible to store such a large sized hash table at each and every node?

- In a DHT, the (key, value) pairs of a large DHT is evenly distributed over peers.
- Each peer only knows about a small number of other peers.
- Also, DHT is robust to network churn.

## How do we implement a DHT?
Navigate through the following pages describing various ways to implement a DHT:
1. [Circular DHT](./circ_dht.md)
2. [Kademlia](./kademlia.md)

### References
- [Link 1](https://www.youtube.com/watch?v=A5Y4HcTp-Ks)
- [Link 2](https://www.youtube.com/watch?v=-UU_ugiPZ9k)

[Back to home](./Home.md)