#cs2105 #notes 
## Learning Objectives
- [ ] Basic terms - ==host, packet, protocol, throughput, store-and-forward, autonomous system==
- [ ] Logical architecture of the internet - ==five protocol layers==
- [ ] Physical architecture of the internet - ==network of ASes==
- [ ] Different components of end-to-end delay and their relationships to bandwidth, packet size, distance, propagation speed and queue size
---

# What is the Internet?

The internet is complex and can be defined in many ways. In this module, internet is viewed as a ==communication== tool.

>[!note]
>The internet is a network of connected computing devices (PC, server, laptop, smartphone) , which are known as ==hosts==or ==end systems==

### Hosts
Hosts run network applications and communicate over links. There are around **1 billion** devices and hosts.

The internet consists of 2 parts – network edge and network core

--- 

# Network Edge (Access Network)

![[accessnetwork.png|50%]]

Hosts access the internet ==through access network== which are different ways to access the internet.

>[!aside | right +++++]
>Switch and hub is used by network edge, not network core

## Home Network
![[homenetwork.png|80%]]
- **Modem**: connect home network to **ISP** network
- **Router**: Set up home network to allow connection from multiple devices by assigning IP addresses to each device

## Enterprise Access Networks (Ethernet)
![[enterpriseaccessnetwork.png|80%]]

## Wireless Access Networks

Wireless access network connect hosts to router via ==base station aka “access point”==

```start-multi-column
ID: ID_rc0y
Number of Columns: 2
Largest Column: standard
Border: off
Shadow: off
```

**Wireless LANs**
- Within building (100ft)
- Commonly known as **Wi-Fi**

>[!note]
>Having many wireless access points in a building will allow you to cover a larger range of area.

--- column-end ---

**Wide-area wireless access**
- Provided by cellular telco operators (10km)
- Commonly known as **3G, 4G**

--- end-multi-column

## Physical Media
Hosts can also connect to access network over different physical media.

**Guided media**
	- Signals propagate in solid media, such as ==twisted pair cable== or ==fiber optic cable==

**Unguided media**
	- Signals propagate freely, ie radio waves

---

# Network Core

A network core is a ==mesh of interconnected routers==. There are no ==direct== users in the network core.

A router is a specially designed computer to ==forward data in the computer network from router to router== through ports in the router.



## Data transmission in networks

>[!aside | right +++++]
>Circuit switching is usually used for ==telephone networks== – not the focus of this module.

### **Circuit Switching** 
Circuit switching is an ==end-to-end== resources allocated to and reserved for *call* between source and destination.
- Call setup is required (to ==reserve== the *circuit*)
- Guaranteed performance (circuit-like performance, since resources are reserved)
- Circuit segment idle if not used by call (==no sharing, simultaneous transmission if there are not sufficient circuits==)
- Commonly used in traditional telephone networks

### **Packet Switching**

>[!aside | right +++++]
>Each packet has a ==maximum size==. For example, NUS network has a packet limit of 1500 bytes. Therefore, for files larger than 1500 bytes, the file will be broken into packets no larger than 1500 bytes.

Packet switching is a ==host sending function== where it breaks application message into smaller chunks, known as ==packets== of length, *L* bits.
- Each bit is sent as a electromagnetic wave (==1 - sine wave, 0 - cosine wave==)
- Each bit is sent ==sequentially==, bit by bit

The packets are transmitted to the link at *transmission rate, R*. The transmission rate is known as **link capacity or link bandwidth**.

>[!aside | right +++++]
>The bandwidth is affected by the ==physical media== and ==encoding==.

>[!note] Packet Transmission Delay
> Packet transmission delay is the time needed to transmit *L*-bit packet into link.
> $$\textsf{Packet transmission delay} = \frac{L \space \textsf{(bits)}}{R \space \textsf{(bits/sec)}}$$

#### **Store-and-forward**
Packets are passed from one router to the next, across links on path from source to destination. The ==entire packet== must arrive at a router before it can be transmitted to the next link. This behaviour is known as ==store-and-forward==.

Suppose there is one router between the `source` and `destination`. There is a transmission delay of $\frac{L}{R}$ from `source` to `router` and another $\frac{L}{R}$ from `router` to `destination`. Therefore, the ==end-to-end delay== = $2 * \frac{L}{R}$.

Despite the delay, store-and-forward is necessary to verify the integrity of the packet before forwarding.

>[!note] Routing and addressing
>Routers determine source-destination route taken by packets, which are determined by the `routing algorithm`. Each packet needs to carry `source` and `destination` information.

>[!caution] Packet switching
> Users’ packets ==share== network resources and resources are used on demand (no dedicated allocation or resource reservation).
> 
> Excessive congestion is possible.
> 
> When the router is overloaded, packets may be dropped.

---

# Internet Structure

The internet is a network of networks.

![[internetstructure.png|80%]]

>[!note]
>**IXP**: internet exchange point

---

# Delay, Loss, Throughput

Routers receive packets from different users and the incoming packets are placed in a ==FIFO queue== in the router buffer. The waiting time for turn to be sent out one by one causes ==packet queuing delay==.

>[!note] What if packet arrival rate exceeds departure rate?
>Suppose the departure rate of the queue in the router is `50 packets/s` and the arrival rate of packets is `100 packets/s`.
>
>New arriving packet will have no buffer space to store and will be lost by the router.

## Packet Loss
- Queue of a router has a finite capacity.
- Packet arriving to ==full queue== will be dropped and **lost**.
- This is known as ==buffer overflow==.

In transmission through media with EM waves (sine wave and cosine wave), there may be differences in `source` and `destination` due to ==noise, interference==. For example, bit `1` sent by `source` may be received as `0` by `destination`. When this occurs, the packet will be dropped by `destination`.

## Packet Delay
There are ==four== sources of packet delay.


```start-multi-column
ID: ID_ciod
Number of Columns: 2
Largest Column: standard
Shadow: off
Border: off
```

### Nodal Processing, $d_{\textsf{proc}}$
- Check bit errors
- Determine output link
- < millisec

--- column-end ---

### Queueing Delay, $d_{\textsf{queue}}$
- Time ==waiting== in the queue for transmission
- Depends on congestion level of router

--- end-multi-column


```start-multi-column
ID: ID_gatb
Number of Columns: 2
Largest Column: standard
Shadow: off
Border: off
```

### Transmission Delay, $d_{\textsf{trans}}$
- *L*, packet length in bits
- *R*, link bandwidth in **bits per second**
- *L/R*

--- column-end ---

### Propagation Delay, $d_{\textsf{prop}}$
- *d*: length of physical link
- *s*: propagation speed in medium
- *d/s*

--- end-multi-column

## End-to-End Packet Delay
==End-to-end== packet delay is the time for a packet to travel from `source` to `destination` and it consists of ==all== four sources of delay.

---

## Throughput
==Throughput== is a measure of how many bits can be transmitted per unit time. This is measured for [[#End-to-End Packet Delay | end-to-end communication]] with multiple links. Link capacity (bandwidth) is meant for a specific link.

---

# Protocol Layers and Service Models

The internet supports various kinds of network applications and exchange messages among peers according to ==protocols==

## Protocol
A ==protocol== defines **format** and **order** of messages exchanged and **actions** taken after messages are sent and received.

>[!note]
>**Protocols** regulate communication activities in a network.

## Internet Protocol Stack
Protocols in computers are **logically** organised into 5 layers according to their purposes.
1. [[Application Layer | Application]]: supporting network application
2. [[Transport Layer]]: Process-to-process data transfer (TCP, UDP)
3. [[Network Layer]]: Routing datagrams from source to destination (IP, routing protocols)
4. [[Link layer]]: Data transfer between neighbouring network elements
5. **Physical**: bits propagated

---
