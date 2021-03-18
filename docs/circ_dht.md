# Circular DHT

- Each peer in the P2P network is assigned an ID.
- A (key, value) pair is assigned or stored in a peer whose ID is *closet* to the key value. *Closet* means the immediate successor of the key.
- Each peer is only aware of the other two peers, i.e., each peer knows the IP address of only two peers - it's successor, and it's predeccesor.

### Resolving a query
- A query is basically asking the question, "What is the value associated with this key?"
- A peer sends the query to its nearest successor. If the neighbor is not responsible for handling the key, it forwards the query to it's successor and it goes on until the peer responsible gets the query.
- The peer then gets the value from it's hash table and sends it directly to the initiator of the query.
- The time complexity is *O(N)* on average to resolve a query, where *N* is the number of peers. **(Big 
disadvantage)**
    - The complexity can be reduced if each peer keeps a track of IP addresses of it's predecessor, successor, and shortcuts (called **circular DHT with shortcuts**). It is possible to design shortcuts such that the total messages of sent to resolve a query is *O(log N)* and the number of neighbors a peer has is *O(log N)*.

### Handling peer churn
- Each peer knows the address of its two successors
- Each peer periodically pings its two successors to check its aliveness
- If the immediate successor leaves, chose next successor as new immediate successor



### References
- [Link 1](https://www.youtube.com/watch?v=-UU_ugiPZ9k)