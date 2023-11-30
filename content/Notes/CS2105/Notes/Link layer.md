>[!aside | right +++++]
> ==Node== : Devices exchanging data (ie hosts, router, etc)
> ==Link==: Communication channels that connect adjacent nodes


>[!note] The aim
>Send data between $N$ nodes via *cable*
>
>Inter-connect the $N$ nodes and send data → Each link needs to be addressed.
>However, inter-connecting every nodes is costly and requires multiple serial ports in a computer. For example, a computer will require $N - 1$ ports
>
>Inter-connect $N$ nodes via a broadcast link → Each link needs to be addressed. For a shared medium, we need to define a *protocol* and handle/ recover from *errors*
---

>[!info] Shared Link
>In an abstract *shared link*, how do we handle:
>1. How a link is *addressed*
>2. How a protocol is *defined*
>3. How *errors* are handled

# Link layer
==Network layer== provides communication service between any two hosts.

An IP datagram may travel through multiple routers and links before it reaches destination.

Link layer sends datagrams between adjacent nodes over a ==single link== and IP datagrams are encapsulated **in link-layer** *frames* for transmission.
>[!caution]
>We are only looking at adjacent nodes

Link layer is strongly coupled to the physical layer and is implemented in the adapter (NIC) or on a chip.

---

## Framing
- Encapsulate datagram in to *frame*, adding header and trailer.

---

## Link access control
- When multiple nodes *share* a single link, need to coordinate which nodes can send frames at a certain point of time

**Type 1: point-to-point link**
- A sender and a receiver connected by a dedicated link

**Type 2: broadcast link (shared medium)**
- Multiple nodes connected to a shared broadcast channel
- When a node transmits a frame, the channel broadcasts the frame and every nodes receive the copy

In a broadcast channel, if two or more nodes transmit simultaneously,
- ==collision== : if a node receives two or more signals at the same time

### Multiple Access Protocols

>[!info] Aim
>Given a broadcast channel of $R$ bps
>
>The ideal multiple access control should be *collision free* and *efficient* — when only one node wants to transmit, it can send at $R$.
>
>It should also be *fair* — when $M$ nodes want to transmit, each can send at an average rate of $R/ M$ and *decentralized* — no special node to coordinate transmission.
>
> >[!caution]
> >Coordination about channel sharing **must** be in the channel itself ( no out-of-band channel signalling )

In order of increasing complexity,
#### Channel partitioning
- Divide channel into fixed, smaller *pieces*
- Allocate piece to node for exclusive use

==Time division multiple access== (TDMA)
- Access to channel in *rounds*
- Each node gets *fixed* length time slots in each *rounds*. For example, every 8 minutes, a node gets 2 minutes if there are 4 nodes

>[!note] 
>==efficient== : inefficient, unused slots go idle
>==fairness== : perfectly fair
>==decentralized== : yes


==Frequency Division multiple access== (FDMA)
- Channel spectrum is divided into frequency bands
- Each *node* is assigned a fixed frequency band
- Unused transmission time in frequency bands go idle

#### Taking turns
- Each node take turns to transmit

##### Polling
Polling protocol requires one of the nodes to be designated as a *master* node and the master node polls each of the nods in a *round-robin* fashion.

If there is data to be transferred, the node can transmit up to maximum number of frames and *master* takes back control

>[!note] 
>==collision-free== : Yes, a node only transfers when it is polled
>==efficient== : The data transmission will be $< R$ for polling operations $\implies$ Highly efficient, but incurs the overhead of polling
>==fairness== : perfectly fair as long as the master is fair
>==decentralized== : Master node is a single point of failure $\implies$ no

---

##### Token
A *special frame*, token, is passed from one node to next sequentially. When a node receives a token, it holds on to the token only if it has some frames to transmit. Otherwise, forward to the next node.

In this protocol, the network topology is known as a *token ring*

>[!note] 
>==collision-free== : Yes, a node only transfers when it is polled
>==efficient== : The data transmission will be $< R$ for polling operations $\implies$ Highly efficient, but incurs the overhead of passing tokens
>==fairness== : perfectly fair as long as the program is fair ( does not hold onto tokens longer than necessary )
>==decentralized== : yes

#### Random access
- Channel is not divided and collisions are possible, need to *recover* from collisions

When a node has data send, it transmits at full channel data rate $R$ with no *a priori* coordination among nodes. Two or more nodes may cause *collision*. The Random access protocols specify how to detect collisions and how to recover from collisions

##### Slotted ALOHA
All frames are of equal size $L$ bits and time is divided into slots of equal length. Nodes start to transmit only at the beginning of a slot.
- Time is synchronised at each node

When the node has a fresh frame to send, wait until the beginning of the next slot and transmits the entire frame in the slot.
- If no collision: data transmission is a success
- Else: data transmission is a failure. Then, both the nodes will retransmit in the subsequent slot with probability $p$ until success
- **DRAWBACK** : the probability of collision in all subsequent time slots remain the same

>[!note] 
>==collision-free== : No
>==efficient== : Efficient, when only one node is active. Slots are wasted due to both collisions and empty slots $\implies$ 36%
>==fairness== : Fair
>==decentralized== : yes

##### Unslotted ALOHA
- Even more simplified than Slotted ALOHA
- Has no time slots and no synchronisation

>[!example]
>When a node has a fresh frame to send,
>1. Transmits the entire frame immediately
>2. If no collision, data transmission is a success
>3. If collision, data transmission is a failure
>	1. It waits for 1 frame transmission time
>	2. Retransmits with probability $p$ until success

**It is not better than Slotted ALOHA**. This is because chance of collision increases.

>[!note]
> ==collision-free== : No
> ==Efficiency== : Yes when only one node is active, $R$. No when there are many active nodes.The max efficiency is only $18\%$. Slots are wasted due to both collision and because of being empty
> ==Fairness== : Perfectly fair
> ==Decentralized== : Yes

>[!caution] Design flaw
>The design flaw in ALOHA is a node’s decision to transmit is made *independently* of the activity of the other nodes attached to the broadcast channel. A node pays no attention to whether another node happens to be transmitting when it begins to transmit

---
### Carrier sensing multiple access
- If channel sensed idle: transmit the entire frame
- If channel sensed busy: defer transmission

#### Propagation delay
2 nodes may not hear each other’s transmission immediately
![[linklayer-collision.png| -s | -center]]

>[!caution] Another design flaw
>One major design flaw in ALOHA and CSMA is that a node does not stop transmitting even when collision is detected.

### CSMA/ CD (Collision detection)
- If channel sensed idle: transmit entire frame
- If sensed busy: defer transmission
- If collision detected: Abort transmission. Retransmit after random delay

![[linklayer-collsioncsma.png| -center | -s]]

If *collision detected*, abort transmission. How to *retransmit* after a random delay? Adapt retransmission attempts to estimated current load (more collisions implies heavier load)

### Backoff algorithm
>[!example]
>After 1st collision:
>- Choose $K$ at random from [0, 1]
>- wait $K$ time units before retransmission
>
>After 2nd collision:
>- Choose $K$ from $\{0, 1, 2, 2^2 - 1\}$
>- Wait $K$ time units before retransmission
>  
> After $m$-th collision
> - Choose $K$ at random from $\{0, 1, … , 2^{m} - 1\}$
> - Wait $K$ time units before retransmission

**Property** : Retransmission attempts to estimate current load
- More collision implies heavier load
- Longer back-off interval with more collisions

The size of frame matters in CSMA

==Frame size too small==: Collision happens but may not be detected by sending nodes $\implies$ no retransmission

>[!aside | right +++++]
>$C$ will receive corrupted data but $D$ and $B$ will not be aware.
>
>*Ethernet* requires a minimum frame size of 64 bytes. 

![[linklayer-nondetection.png| -s | -center]]

>[!note]
> ==collision-free== : No
> ==Efficiency== : Yes
> ==Fairness== : Yes
> ==Decentralized== : Yes

---

## Error detection
- Errors are usually caused by signal attenuation or noise
- Receiver detects presence of errors and signal for retransmission or simply drops frames

Data transfer is over an unreliable medium and is bit-error prone. In a datagram, we append with ==Error Detection and Correction bits== (EDC).

| data bits |     |
| --------- | --- |
| D         | EDC |
where $D$ is data protected by error checking and may include header fields

![[EDC.png| -s | -center]]
- EDC can be $D$ itself
---

### Parity checking
Suppose the information to be sent $D$ has `d` bits.

In an ==even parity== scheme, the sender simply includes one additional bit and we choose its value such that the total number of `1s` in the $d + 1$ bits is even. The additional bit becomes the *parity bit*

- Can detect *single bit* errors in data or *odd number* of single bit errors
- If errors are *independent*, probability of multiple bit errors is ==low==
However, errors are often clustered together in ==bursts==. The probability of *undetected errors* in a frame can approach is $50 \%$

### Parity checking in 2D
Arrange the `d` bits in $i$ rows and $j$ columns.
A parity value is computed for each row and for each column. The resulting $i + j + 1$ parity bits comprise the link-layer’s error detection bits.

![[2dparity.png| -s | -center]]
In the example above, the parity bits of column and row is $2 + 2$ so the parity bit is $0$.
>[!note]
>A flipped bit will cause the parity bit in the row and column of that bit to be different.

- Can detect **AND** correct single bit errors in data
- Can detect *any* two-bit error in data

---
### Cyclic Redundancy Check (CRC)
Augment with $R$ : the $r$ digit error detection code

>[!note] Aim
>Generate $R$ such that the sender can compute $R$ easily and the receiver can verify the integrity of $D$ easily $\implies$ use a special $r$ digit number $G$ called the *Generator*

>[!caution]
>The following is for non-binary digits


>[!example] 
>On the **sender**,
>$D = 21027845, \enspace r = 3, \enspace G = 401$
>1. Append $r \enspace 9’s$ to $D$
>2. Find the remainder $y$ of $\frac{X}{G}$
>3. $M = X - y$
>4. $M$ is now divisible by $G$
>
>Now, the 8-digit data is still preserved, but we have augmented such that it is divisible by $G$.
>
>On the **receiver**, the received message $M$ should be divisible by $G$
>1. Find the remainder
>2. If remainder = 0, then no error is detected
>3. Else, the data is faulty and discard.

$G$ should be chosen **prime number**
We append with 3 9’s so that no matter how it is subtracted, it will not overflow into $D$ that we wish to send.

For *binary data*, let $D$ be data bits, viewed as binary number, $G$ be the generator of $r + 1$ bits, agreed by sender and receiver beforehand and $r$ bit CRC.
- Calculations are done in *mod 2*
- In performing division, we append $r$ 0’s to $D$
>[!example] 
>$D = 101110, \enspace r = 3, \enspace G = 1001$
>1. Augment $D$ with $3 \enspace 0’s$
>2. Divide $D$ by $G$, using bitwise XOR for subtraction to find the remainder $y$
>3. Note that CRC appended is always just the remainder
>
>On the **receiver**, $(D, R)$ is divided by $G$

Since we do not care what is the *carry bit* in XOR operations, we can parallelise the operation and easy to implement on hardware.

- Powerful error-detection coding that is widely used in practice
- Can detect *all odd numbers* of single bit errors
- CRC of *r* bits can detect all burst errors of less than $r+1$ bits
- All burst errors of greater than $r$ bits with probability $1 - 0.5^r$
- This is also known as *Polynomial code*

---
## Error correction
- Receiver identifies and correct bit error(s) without resorting to retransmission

## Reliable delivery
- Often used on error-prone links such as wireless links