# Circular DHT RPC Syntax

All the RPCs have the following format
```
<RPC-identifier>:<sender-lportNo>:<data-1>:<data-2>:...:<data-n>
```
`<sender-lportNo>` refers to the listening port number of the node that sends a particular RPC to another node. In this way, the sender is informing the receiver to which port number the receiver must reply to.
The meaning of `<data-1>, <data-2>, ..., <data-n>` is dependent on the RPC.

## General RPCs
| RPC | Message Syntax |
| --- | --- |
| **<INVALID-RPC\>** | !:<sender-lportNo\> |

## Joining the network
| RPC | Message Syntax |
| --- | --- |
| **<JOIN-NETWORK\>** | J:<sender-lportNo\> |
| **<UPDATE-SUCCESSOR-PREDECESSOR\>** | USP:<sender-lportNo\>:<successor-lportNo\>:<predecessor-lportNo\> |
| **<UPDATE-SUCCESSOR\>** | US:<sender-lportNo\>:<new-successor-lportNo\>|
| **<UPDATE-PREDECESSOR\>** | UP:<sender-lportNo\>:<new-predecessor-lportNo\>|

## Data Manipulation
| RPC | Message Syntax |
| --- | --- |
| **<TRANSFER-KEYS\>** | T:<sender-lportNo\>|
| **<STORE-KEY\>** | SK:<sender-lportNo\>:<lportNo-node-wanting-to-store\>:<key\>|
| **<GET-VALUE\>** | G:<sender-lportNo\>:<key-whose-value-is-needed\>:<D/ND\>|
| **<STORE-KEY-VALUE\>** | SV:<sender-lportNo\>:<key\>:<value\>:<ST/SH\>|
| **<SHOW-KEYS\>** | SHW:<lportNo-of-node-wanting-keys\>|
| **<KEYS-RECEIVED\>** | KR:<sender-lportNo\>:<list-of-all-its-keys\>:<NP/PE/PNE\>|