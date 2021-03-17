# Overview of peer-to-peer networks

## Definitions
The following definitions are quoted from this [paper][1].
### Def1 | Peer-to-Peer Network
A distributed network architecture may be called a peer-to-peer network if the participants share a part of their own hardware resources (processing power, storage capacity, network link capacity, printers, etc.). These shared resources are neccesary to provide the service and content offered by the network (e.g: file sharing or shared workspaces for collaboration). They are accessible by other peers directly, without passing intermediary entities. The participants of such a network are thus resource providers as well as resource requestors.

### Def2 | Pure Peer-to-Peer Network
A distributed network architecture has the classified as a *pure* P2P network, if it is firstly a P2P network according to **def1**, and secondly if any single, arbitrary chosen terminal entity can be removed from the network without having the network suffering any loss of network service.

### Def3 | Hybrid Peer-to-Peer Network
A distributed network architecture has the classified as a *hybrid* P2P network, if it is firstly a P2P network according to **def1**, and secondly a central entity is necessary to provide parts of the network services.

### Def4 | Client/Server Network
A client/server network is a distributed network which consists of one higher performance system, the Server, and several mostly lower performance systems, the Clients. The Server is the central registering unit as well as the only providder of content and service. A Client only requests content of the execution of services, without sharing any of its own resources.

## More about P2P network
Source : [Link][2]
- The power of P2P is apparent when considering Metcalfe’s Law
> The value of a network is proportional to the square of the number of connected users
- The number of possible connections within a P2P network can
be exponential in relation to the number of network nodes, *n*. All nodes can potentially connect to all other nodes, giving a theoretical maximum number of connections of n(n − 1)/2; the same number as in a fully connected mesh network.
### Aim of a P2P network
> To host resources at one or more peers in a network *(a storage function)* and to allow other peers to find these resources *(a routing function)* in a distributed space.
- The resouces can be viewed as “values” and the search characteristics used to locate the resources can be viewed as “keys”.
The function of a P2P network can be specified as a pair of methods:
    - **put(key, value)**: *store a value with an associated key (or
set of keys) in the network*
    - **value = get(key)**: *retrieve the value given a key at some later time*
- Types of P2P networks:
    - Structured
        - The joining peer is admitted based on an identifier that places the joining peer in relation to a set of existing peers
        - Characterized as forming a Distributed Hash Table (DHT)
        - Each peer is responsible for a certain portion of the namespace where the keys are hashed. The result of this deterministic hashing is that there exists a strict upper bound on the search time for a resource.
    - Unstructured
        - Do not impose a strict formation on the peers themselves; a joining peer could simply connect to any existing peer to become part of the P2P network.
        - Use blind flooding and random walks to search for the resource.

## Key features of a P2P network
1. Each peer (node) in a P2P network knows typically a small number of its neighbors. A peer’s neighbors are the possible routes for forwarding
messages, and they also act as gateways to receive responses from the network. The neighbors of a peer are directly reachable. Routes beyond these neighbors provide connectivity to the entire P2P network as a whole. Peers need to keep track of their neighbors to ensure that they still remain connected to the P2P network. Peers may need to drop existing neighbors, or request new neighbors, throughout the duration of their P2P session to ensure that they remain connected to the network.
2. The action of peers arriving and leaving is called **network churn**. Churn is induced by “willing” actions, for example, node departures and mobility, and also “unwilling” actions, such as inadvertent failure of a node. High levels of churn indicate many peers coming and going frequently, while low levels exhibit longer peer session durations with less frequent arrivals and departures.
3. **Seeders** (peers that have the entire content) may stay connected to the swarm (P2P network) for a longer period of time, while **leechers** (peers that have portions of the content) may connect with the swarm until the content is downloaded and then leave the swarm. For a swarm to continue serving content, the leechers may have to act altruistically by becoming seeders after acquiring the complete content.
4. To process of gaining access and becoming a participant in the P2P network is known as **bootstrapping**. Peers will bootstrap using some kind of centralized resource, commonly called a **bootstrapping node** or **rendezvous host**, which gives the unconnected peer an entrance point into the network in the form of a set of active network member addresses.
5. To keep track of other peers and possible routes, a local collection of peer addresses is managed via a routing table. A **routing table** may indicate a neighbor’s address directly, or alternatively via a next hop in a multihop route, and also associates a cost with each potential path.

## Pros and Cons
### Pros
- Scalability
- High resource availability
- No need for a centralized authority (eliminating a single point of failure)
- Robustness
-  As each node in the network operates as both a client and a server, it promotes incentives to participate rather than spectate within the system

### Cons
- Consequence of using a P2P architecture is that the quality and usefulness of the services on offer rely entirely on the participating members of the group
- Ensuring that viruses are not introduced to the network is the responsibility of each individual node
- Since there is no way to authenticate the data being transferred around P2P networks, illegal material may be shared

### On overlay network
> Source: Wikipedia

An overlay network is a computer network that is layered on top of another network. Nodes in the overlay network can be thought of as being connected by virtual or logical links, each of which corresponds to a path, perhaps through many physical links, in the underlying network. For example, distributed systems such as peer-to-peer networks and client-server applications are overlay networks because their nodes run on top of the Internet.

The Internet was originally built as an overlay upon the telephone network, while today (through the advent of VoIP), the telephone network is increasingly turning into an overlay network built on top of the Internet.


[Back to home](./Home.md)

[1]:10.1109/P2P.2001.990434
[2]:https://dl.acm.org/doi/10.1145/2501654.2501660