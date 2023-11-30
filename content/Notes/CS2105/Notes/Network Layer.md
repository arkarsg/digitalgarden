>[!note] IP address
>Every computer has an IP address

# Network layer services

Network layer delivers packets to receiving hosts. ==Routers== examine header fields of IP datagrams passing it.

![[networklayerservics.png| -m | -center]]

## IP address

==IP address== is used to identify a host (or a router)
- 32-bit integer expressed in either binary or decimal

## Dynamic Host Configuration Protocol

>[!note]
>Host can get an IP address manually configured by system administrator, or, *automatically assigned* by a ==DHCP== server

==DHCP== allows a host to dynamically obtain its IP address from DHCP server when it joins the network
- IP address is renewable
- DHCP only hold address while connected and reuse is allowed
- Support mobile users who want to join network

**In addition** to host IP address assignment, DHCP may also provide a host additional network information:
1. IP address of first-hop router
2. IP address of local DNS server
3. Network mask (indicating network prefix vs Host ID of an IP address)

>[!note] DHCP runs over UDP
>DHCP server port number = `67`
>DHCP client port number = `68`

### 4-step process
1. Host broadcasts ==DHCP discover== message
2. DHCP server responds with ==DHCP offer== message
3. Host request IP address with ==DHCP request== message
4. DHCP server sends address with ==DHCP ACK== message

![[DHCPack.png| -center | -m]]

## Network interface
>[!note]
>An IP address is associated with a *network interface*

A *host* usually has one or two network interfaces (ie wired ethernet and WiFi)
- A router typically has multiple interfaces

![[subnets.png| -s | -center]]

## IP address and subnet
An IP address logically comprises of two parts:

| 32-bits                 |               |
| ----------------------- | ------------- |
| n bits                  | (32 - n) bits |
| network (subnet) prefix | host ID       | 

A ==subnet== is a network formed by a group of *directly* interconnected hosts.
- Hosts in the *same* subnet have the same network prefix of IP address
- Hosts in the same subnet can *physically* reach each other without intervening router
- They are connected to the outside through a router

## CIDR
The Internet’s IP address assignment strategy is known as ==Classless Inter-domain Routing== (CIDR). It has the following format:
- Subnet prefix of IP address is of arbitrary length
- Address format: `a.b.c.d/x` where `x` is the number of bits in subnet prefix of IP address

![[subnetprefix.png| -m | -center]]

### Subnet mask
A ==subnet mask== is used to determine which subnet an IP address belongs to.

![[subnetmask.png| -m | -center]]

### IP address allocation

An *organisation* obtains a block of IP addresses by buying from registry or rent from ISP’s address space.

An *ISP* get a block of address from Internet Corporation for Assigned Names and Numbers (==ICANN==)
- Allocate addresses
- Manages DNS
- Assigns domain names, resolves disputes

![[subnetorganisation.png| -m | -center]]

#### Special IP Addresses

![[specialipaddr.png| -m | -center]]


### Hierarchical addressing

![[subnetrouters.png| -m | -center]]

### Longest prefix match

Suppose a packet is at a router `Router R3`. Then, the router may have the following *forwarding table*:

| **Net mask**   | **Next hop** |
| -------------- | ------------ |
| 200.23.16.0/20 | R1           |
| 200.23.18.0/23 | R2           |
| 199.31.0.0/16  | R2           |

If a packet has destination IP `200.23.20.2`:
```plain-text
1. Represent as binary

packet p =   11001000 00010111 00010100 00000010

2. Represent net mask in binary

netmask n1 = 11001000 00010111 00010000 00000000
netmask n2 = 11001000 00010111 00010010 00000000
netmask n3 = 11001000 00010111 00000000 00000000

3. Choose the net mask that has the longest prefix match --> n1
```

Therefore, the packet will be forwarded to $R_1$

---

If a packet has destination IP `200.23.19.3`:
```plain-text
1. Represent as binary

packet p =   11001000 00010111 00010011 00000010

2. Represent net mask in binary

netmask n1 = 11001000 00010111 00010000 00000000
netmask n2 = 11001000 00010111 00010010 00000000
netmask n3 = 11001000 00010111 00000000 00000000

3. Choose the net mask that has the longest prefix match --> n2
```

Therefore, the packet will be forwarded to $R_2$

---

# Routing in the internet
>[!note] The internet
>The internet is a network-of-networks which has a hierarchy of *autonomous systems* (AS)
>
>Due to the size of the internet and the decentralised administration of the internet, routing on the internet is done hierarchically.

## Intra-AS routing
- Finds a good path between two routers within an AS
- Commonly uses *RIP, OSPF*
- Single admin → no policy decisions are needed
- Routing mostly focus on performance

---

## Routing algorithm
>[!caution] Routing
>Finding a *least cost path* between two vertices in a graph

- All routers have the complete knowledge of network topology and link cost
	- Routers periodically broadcast link costs to each other

- Routers know physically-connected neighbours and link costs to neighbours
- Routers exchange *local views* with neighbours and update own *local views* based on neighbour’s views

### Distance vector algorithm

==Iterative process of computation==
1. Swap local view with direct neighbours
2. Update own’s local view
3. Repeat 1-2 until no more change to local view

- Routers know *physically-connected* neighbours and link costs to neighbours
- Routers exchange *local views* with neighbours and update own *local views* based on neighbour’s views

### Optimal substructure of Bellman Ford
- Let $c(x, y)$ be the cost link between routers $x$ and $y$ that are direct neighbours
- $d_x(y)$ the cost of the least-cost path from $x$ to $y$.

$$
d_{x}(y) = \min_{v} \{ c(x,v) + d_v(y) \}
$$
In other words, to find the least cost path, $x$ needs to know the cost from each of its direct neighbour to $y$

Each neighbour $v$ sends its *distance vector* $(y, k)$ to $x$ about the cost from $v$ to $k$ which is $k$

---

## Distance vector algorithm
Every router $x, y, z$ sends its distance vectors to its directly connected neighbours.

When $y$ sends its distance vector to $z$ that is cheaper than what $x$ already knows,
1. $x$ will update its distance vector to $z$ accordingly
2. $x$ will note that for packets sent to $z$, it should also be sent to $y$. This creates the forwarding table of $x$
After every router has exchanged several rounds of updates with its direct neighbours, all routers will know the least-cost paths to all the other routers.

---

# Routing information protocol
==RIP== implements the DV algorithm using the *hop count* as the cost metric.
- Insensitive to network congestion
- It exchanges routing table every 30 seconds over UDP port 520
- *Self-repair* : if no update from a neighbour router for 3 minutes, assume neighbour has failed.

---

# Network Address Translation

![[nat.png| -m | -center]]

NAT routers **MUST**:
1. *Replace* `(source IP, port#)` of every *outgoing datagram* to `(NAT IP address, new port#)`
2. *Remember* in the ==NAT translation table== the mapping from `(source IP address, port#)` to `(NAT IP address, new port#)`
3. *Replace* `NAT IP address, new port#)` in destination field of every *incoming datagram* with corresponding `(source IP address, port#)` stored in NAT translation table.

![[natexample.png| -m | -center]]

## Motivation
- There is no need to rent a range of public IP addresses from ISP → just 1 public IP for the NAT router
- All hosts use private IP addresses, and can change addresses of hosts in local network without notifying the outside world
- Can change ISP without changing addresses of hosts in local network
- Hosts inside local network are not explicitly addressable and visible by outside world

---

# Internet Protocol (IP)

## IPv4 Datagram format
![[ipv4datagram.png| -m | -center]]

## IP fragmentation and reassembly
>[!note]
>Different links may have different *Max Transfer Unit* (MTU) which is the maximum amount of data a link-level frame can carry

If the IP datagram is too large, the IP datagram may be fragmented by routers.

Destination host will reassemble the packet and ==IP header fields== are used to identify fragments and their relative order

![[fragment.png| -s | -center]]

![[fragheader.png| -m | -center]]

---
**Frag flag** : set to `1` if there is a next fragment from the same segment, `0` if it is the last segment

**Offset** is expressed in unit of 8 bytes

![[fragoffset.png| -m | -center]]

---
# Internet Control Message Protocol (ICMP)

>[!note]
>Used by hosts and routers to communicate ==network-level== information
>	- Error reporting: unreachable host / network / port / protocol
>	- Echo request / reply (used by `ping`)

ICMP messages are carried in IP datagrams.
>[!info]
>ICMP header starts after IP header

## ICMP Type and code
>[!caution] ICMP header
>ICMP header consists of `type`+ `code` + `checksum` + others…

| Type | Code | Description           |
| ---- | ---- | --------------------- | 
| 8    | 0    | Echo request (ping)   |  
| 0    | 0    | Echo reply (ping)     | 
| 3    | 1    | dest host unreachable |    
| 3    | 3    | dest port unreachable |    
| 11   | 0    | TTL expired           |    
| 12   | 0    | bad IP header         |    

For example, when **TTL** is 0, a packet is discarded and an ICMP error message is sent to the datagram’s *source* address.

### `ping` and `traceroute`
- The command `ping` sees if a remote host will respond to us (ie whether we have a connection)
- The command `traceroute` sends a *series of small packets* across a network and attempts to display a route or a path that the messages would take to get to a remote host.
---

