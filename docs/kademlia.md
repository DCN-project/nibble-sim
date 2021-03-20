# Kademlia

## Structure
- Minimizes the number of configuration messages nodes must send to learn about each other
- 160-bit node IDs
- 160-bit keys (generated using SHA-1 hash)
- (key,value) pairs are stored on
nodes with IDs *close* to the key
- Uses XOR metric for distance between points in the key space
- To locate nodes near a particular ID, Kademlia uses a single routing algorithm from start to finish
- Kademlia effectively treats nodes as leaves in a binary tree, with each node’s position determined by the shortest unique prefix of its ID
- For any given node, we divide the binary tree into a series of successively lower subtrees that don’t contain the node
- The Kademlia protocol ensures that every node knows of at least one node in each of its subtrees, if that subtree contains a node
- Every message a node transmits includes its node ID, permitting the recipient to record the sender’s existence if necessary
- Given two 160-bit identifiers, x and y, Kademlia defines the distance between them as their bitwise XOR interpreted as an integer, d(x, y) = x ⊕ y.
- For each 0 ≤ i < 160, every node keeps a list of (IP address, UDP port, Node ID) triples for nodes of distance between 2^i and 2^(i+1) from itself. We call these lists k-buckets.
- Each k-bucket is kept sorted by time last seen node
    - least recently seen node at head
    - most-recently seen at the tail. 
- For large values of i, the lists can grow up to size k, where k is a system-wide replication parameter. k is chosen such that any given k nodes are very unlikely to fail within an hour of each other (for example k = 20).
- When a Kademlia node receives any message (request or reply) from another node, it updates the appropriate k-bucket for the sender’s node ID as follows:
    - If the sending node already exists in the recipient’s k-bucket, the recipient moves it to the tail of the list.
    - If the node is not already in the appropriate k-bucket and the bucket has fewer than k entries, then the recipient just inserts the new sender at the tail of the list.
    - If the appropriate k-bucket is full, however, then the recipient pings the k-bucket’s least-recently seen node to decide what to do:
        - If the least-recently seen node fails to respond, it is evicted from the k-bucket and the new sender inserted at the tail.
        - If the least-recently seen node responds, it is moved to the tail of the list, and the new sender’s contact is discarded.
- Benefit of k-buckets is that they provide resistance to certain DoS attacks. One cannot flush nodes’ routing state by flooding the system with new nodes. Kademlia nodes will only insert the new nodes in the k-buckets when old nodes leave the system.

## The Kademlia protocol
> In distributed computing, a **remote procedure call** (RPC) is when a computer program causes a procedure (subroutine) to execute in a different address space (commonly on another computer on a shared network), which is coded as if it were a normal (local) procedure call, without the programmer explicitly coding the details for the remote interaction. That is, the programmer writes essentially the same code whether the subroutine is local to the executing program, or remote.

- Four RPCs in Kademlia protocol:
    1. **PING**: probes a node to see if it is online.
    2. **STORE**: instructs a node to store a ⟨key, value⟩ pair for later retrieval.
    3. **FIND-NODE**: takes a 160-bit ID as an argument. The recipient of the RPC returns ⟨IP address, UDP port, Node ID⟩ triples for the k nodes it knows about closest to the target ID. These triples can come from a single k-bucket, or they may come from multiple k-buckets if the closest k-bucket is not full. In any case, the RPC recipient must return k items (unless there are fewer than k nodes in all its k-buckets combined, in which case it returns every node it knows about).
    4. **FIND-VALUE**: returns (IP address, UDP port, Node ID) triples—with one exception: if the RPC recipient has received a store RPC for the key, it just returns the stored value.
    - In all RPCs, the recipient must echo a 160-bit random RPC ID, which provides some resistance to address forgery. *PINGS* can also be piggy-backed on RPC replies for the RPC recipient to obtain additional assurance of the sender’s network address.

### Node lookup procedure
- Kademlia employs a recursive algorithm for node lookups.
- The lookup initiator starts by picking α nodes from its closest non-empty k-bucket (or, if that bucket has fewer than α entries, it just takes the α closest nodes it knows of).
- The initiator then sends parallel, asynchronous *find-node* RPCs to the α nodes it has chosen. α is a system-wide concurrency parameter, such as 3.
- In the recursive step:
    - the initiator resends the *find-node* to nodes it has learned about from previous RPCs. (This recursion can begin before all α of the previous RPCs have returned).
    - Of the k nodes the initiator has heard of closest to the target, it picks α that it has not yet queried and resends the *find-node* RPC to them.
    - Nodes that fail to respond quickly are removed from consideration until and unless they do respond. If a round of *find-nodes* fails to return a node any closer than the closest already seen, the initiator resends the *find-node* to all of the k closest nodes it has not already queried.
    - The lookup terminates when the initiator has queried and gotten responses from the k closest nodes it has seen.
    - Kademlia can route for lower latency because it has the flexibility of choosing any one of k nodes to forward a request to.

### Storing key-value pair
- A participant locates the k closest nodes to the key and sends them *STORE* RPCs.
- Additionally, each node re-publishes (key,value)
pairs as necessary to keep them alive.

### Finding key-value pair
- To find a (key,value) pair, a node starts by performing a lookup to find the k nodes with IDs closest to the key. However, value lookups use *FIND_VALUE* rather than *FIND_NODE* RPCs.
- Moreover, the procedure halts immediately when any node returns the value.
- For caching purposes, once a lookup succeeds, the requesting node stores the (key,value) pair at the closest node it observed to the key that did not return the value. Because of the unidirectionality of the topology, future searches for the same key are likely to hit cached entries before querying the closest node. During times of high popularity for a certain key, the system might end up caching it at many nodes.

### Joining a network
- A node *u* must have a contact to an already participating node *w*.
- *u* inserts *w* into the appropriate k-bucket.
- *u* then performs a node lookup for its own node ID.
- Finally, *u* refreshes all k-buckets further away than its closest neighbor. During the refreshes, *u* both populates its own k-buckets and inserts itself into other nodes’ k-buckets as necessary.

## Routing table
- The routing table is a binary tree whose leaves are k-buckets.
- Each k-bucket contains nodes with some common prefix of their IDs. The prefix is the k-bucket’s position in the binary tree. Thus, each k-bucket covers some range of the ID space, and together the k-buckets cover the entire 160-bit ID space with no overlap.

## Efficient key re-publishing
### The need
- To ensure the persistence of key-value pairs, nodes must periodically republish keys. Otherwise, two phenomena may cause lookups for valid keys to fail:
    1. some of the k nodes that initially get a key-value pair when it is published may leave the network.
    2. new nodes may join the network with IDs closer to some published key than the nodes on which the key-value pair was originally published.
- In both cases, the nodes with a key-value pair must republish it so as once again to ensure it is available on the k nodes closest to the key.
