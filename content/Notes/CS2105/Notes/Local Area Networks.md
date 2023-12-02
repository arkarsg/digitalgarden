>[!note] Link layer
>Ethernet is part of [[Link layer]]

- [ ] The role of switches in interconnecting subnets in a LAN
- [ ] how ARP allows a host to discover the MAC addresses of other nodes in the same subnet
---
# MAC address
>[!note] MAC address
>MAC stands for Media Access Control

Every adapter (NIC) has a MAC address (aka physical or LAN address). MAC address is typically *48 bits* burned in NIC ROM (*Read-only memory*).
>[!caution]
>If the device is a virtual machine, then the MAC address can be changed

- Used to send and receive link layer frames
- When an adapter receives a frame, it checks if destination MAC address of the frame matches its own MAC address
	- If *yes*, adapter extracts the enclosed datagram and passes it to the protocol stack
	- If *no*, adapter simply discards the frame without interrupting the host

>> `5C-F9-DD-E8-E3-D2` (hexadecimal notation of a MAC address)
>> `FF-FF-FF-FF-FF-FF` (hexadecimal notation of a broadcast MAC address)

- MAC address needs to be **unique** and the address allocation is administered by IEEE.
	- First 3 bytes identifies the vendor of an adapter
---
# Ethernet

## Local Area Network (LAN)
LAN is a computer network that interconnects computers within a *geographical area* such as office building or university campus (ie a single network).
### 802.3 Ethernet standards
A series of Ethernet standards have been developed over the years and depends on the choice of physical media and different speeds (2 Mbps to 100 Gbps)
- *MAC protocol* and *frame format* remains unchanged

## Ethernet Frame Structure
What happens when we send an *IP* datagram from one host to another, on the same Ethernet LAN?

- The sending NIC (adapter) encapsulates *IP* datagram in ==Ethernet frame==.

![[lan-macaddress.png|80%]]

**Preamble** : 7 bytes with pattern `10101010`, followed by 1 byte with pattern `10101011` also called *start of frame*. Used to synchronise receiver and sender clock rates.

The preamble provides a *square wave* pattern that tells the receiver the sender’s clock rate. This also tells the receiver the width of a bit.

**Source and dest MAC address** : If NIC receives a frame with matching dest or with broadcast addr → pass data in the frame to upper layer. Else, discard

**Data** : Max size is 1500 bytes. The maximum size is the link [[Network Layer#IP fragmentation and reassembly | MTU]]. The minimum size is 46 bytes to ensure that a collision will always be detected.

**CRC** : Corrupted frame will be dropped.

**Type** : Indicates higher layer protocol. This is because hosts can use other network-layer protocols beside IP. The type field permits Ethernet to multiplex network-layer protocols.

---
## Data Delivery Service
**Unreliable** : Receiving NIC does not send ACK or NAK to sending NIC
- Data in dropped frames will be recovered only if initial sender uses higher layer rdt (ie TCP), otherwise, dropped data is lost

**Multiple access protocol** : CSMA/ CD with binary exponential backoff

---
# Physical topology
How do we interconnect nodes to create this shared link?

## Bus topology
The *original* ethernet LAN used a coaxial bus to interconnect the nodes and is a broadcast LAN
- All transmitted frames received by all adapters connected to the bus. All nodes can collide with each other.
- Backbone cable : If damaged, the entire network will fail
- Difficult to troubleshoot problems
- Very slow and not ideal for larger networks (due to collisions)

## Hub
*Hub* enables the creation of *star* topology — where there is a central device to which all devices are connected and all devices communicate via this intermediary
- Nodes are directly connected to a hub
- Is a *physical layer* device that acts on individual bits rather than frames
- Cheap and easy to maintain due to modular design of the network
- Very slow and not ideal for larger networks due to collision

The hub simply re-create the bits and boosts its energy, strength and transmits the bit onto all the other interfaces. In other words, hub works like a logical bus.

## Switch
*Switch* also enables the creation of star topology — is still prevalent today.
- A switch is a *layer-2* device, that is it acts on *frames* rather than individual bits
- No collisions
- A bona-fide *store-and-forward* packet switch

---
# Ethernet Switch
A *link layer* device used in LAN and can examines incoming frame’s MAC address and *selectively forward* frame to one-or-more outgoing links (improves the efficiency of the device).
- Store-and-forward ethernet frames : can handle buffering and heavier loads
- Uses CSMA/CD to access link (can recover from collision)

**Transparent device** where hosts are unaware of presence of switches
>[!example]
>Suppose hosts $A$ and $B$ and a switch through which $A$ and $B$ are connected. A frame will hop on the switch and selectively forwarded to $B$.
>
>A switch neither creates an ethernet frame nor is any frame addressed to the switch.
>
>$A$ logically thinks that a frame is directly sent to $B$

**Plug-and-play** : switches do not need to be configured

### Multiple simultaneous transmissions
Nodes have dedicated, direct connection to switch and switches buffer packets.

Ethernet protocol used on each incoming link but no collisions.

>[!example]
>$A$-to-$A’$ and $B$-to-$B’$ can transmit simultaneously without collisions

### Interconnecting switches
Switches can be connected in hierarchy

To create a LAN,
![[lan-lan.png|80%]]
![[lan-to_internet.png| -m | -center]]
### Selective forwarding
How does switch know $A$ is reachable via interface 1?
Each switch has a *switch table*
`(MAC address of host, interface to reach host, TTL)`

However, routing protocol is not necessary. Use *self-learning* instead

>[!example]
>Switch table is initially empty. Switch *learns* which hosts can be reached through interfaces
>
>When a frame is received, switch leans the location of sender. and records sender/location pair in switch table.

### Frame filtering/ forwarding
![[lan-switchtable.png|80%]]

```
Record incoming link, MAC address of sending host
Index switch table using MAC destination address
If entry found for destination
	if destination on segment from which frame arrived
		drop frame
	else
		forward frame on interface indicated by entry
else
	flood to all interface except the arriving interface
```

---
![[lan-switchvsrouters.png|80%]]

---
# Address Resolution Protocol (ARP)
>[!question] How to know the MAC address of a receiving host, knowing its IP address?
>Use ARP [RFC 826]. Provides a query mechanism to learn the MAC address

Each IP *node* has an ==ARP table== and stores the mapping of IP address and MAC address of other nodes in the same subnet.
>> `IP address, MAC address, TTL`

---

Suppose $A$ wants to send data to $B$, and they are in the ==same== subnet.

1. If $A$ knows $B$‘s MAC address from its ARP table,
	- Create a frame with $B$‘s MAC addresses and send it
	- Only $B$ will process this frame
	- Other nodes may receive but will ignore this frame
2. If $A$ is not aware of $B$:
	- $A$ broadcasts an ARP query packet containing $B$‘s IP address.
	- Destination MAC address set to `FF:FF:FF:FF:FF:FF`
	- All other nodes will receive the ARP query but only $B$ will reply to it
	- $B$ replies to $A$ with its MAC address and reply frame is sent to $A$‘s MAC address. $B$ knows who to reply to with the `source` MAC address.
	- $A$ caches $B$‘s IP-to-MAC address mapping in its ARP until TTL expires
---
Suppose $A$ wants to send to $B$ in ==another== subnet

1. $A$ creates IP datagram with IP source $A$, destination $B$
2. $A$ creates link-layer frame with $R$‘s MAC address as destination address
3. Frame is sent from $A$ to $R$
4. $R$ forwards datagram with MAC source $R$, IP source $A$, destination $B$
5. $R$ creates a link-layer frame with $B$‘s MAC address as destination address

---
```start-multi-column
ID: ID_a0e8
Number of Columns: 2
Largest Column: standard
Border: off
Shadow: off
```
### IP address
- 32 bits in length
- Network-layer address used to move datagrams from source to dest
- Dynamically assigned; hierarchical


--- column-end ---

### MAC address
- 48 bits in length
- Link-layer address used to move frames over every single link
- Permanent, to identify hardware

--- end-multi-column



