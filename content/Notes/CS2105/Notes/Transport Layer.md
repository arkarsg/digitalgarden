# Services

- Deliver messages between application processes running on different hosts with [[Transport Layer#TCP]] and [[Transport Layer#UDP]].

- Transport layer *protocols* run in hosts

```start-multi-column
ID: ID_s80t
Number of Columns: 2
Largest Column: standard
Border: off
Shadow: off
```

### Sender
- Breaks application message into segments (as needed) and passes them to ==network layer==.

--- column-end ---

### Receiver
- Reassembles segments into messages and passes it to application layer

--- end-multi-column


```start-multi-column
ID: ID_aky6
Number of Columns: 2
Largest Column: standard
Border: off
Shadow: off
```

### Packet switching
Packet switches routers in between which only check destination IP address to decide routing.


--- column-end ---

--- end-multi-column

## Transport/ Network layers
>[!info] IP datagram
>Each IP datagram contains *source* and *destination* IP addresses

---

# UDP

^a99614

>[!note] UDP
>UDP stands for User Datagram Protocol.

**Why is there UDP?**
- No connection establishment (which can add delay)
- Simple; no connection state at sender, receiver
- Small header size
- No congestion control

UDP adds very little service on top of IP:

**Multiplexing at sender** : UDP gathers data from processes, forms packets and passes them to IP

**De-multiplexing at receiver** : UDP receives packets from lower layer and dispatches them to the right porcesses.

>[!note] Connectionless de-multiplexing
>When *UDP receiver* receives a UDP segment, it checks the *destination port number* in segment, *directs* UDP segment to the socket with that port number.
>
>IP datagrams (from different sources) with the same destination port number will be directed to the same UDP socket at destination.



**Checksum**

>[!caution] Transmission
>UDP transmission is unreliable

---

## UDP Header

Format of UDP header

**Length** includes the header size (32 bits) and the payload.


| 16 bits            | 16 bits                 |
| ------------------ | ----------------------- |
| source port number | destination port number |
| length             | checksum                |

---

## UDP Checksum

>[!aside | right +++++]
>If packet size is not multiple of 16 bits, pad with trailing zeroes

>[!note]
>Goal of ==checksum== is to detect errors (flipped bits) in transmitted segment


```start-multi-column
ID: ID_56cz
Number of Columns: 2
Largest Column: standard
Border: off
Shadow: off
```

### Sender
- Compute checksum value
- Put checksum value into UDP checksum field


--- column-end ---

### Receiver
- Compute checksum of received segment
- Check if computed checksum equals checksum field value

--- end-multi-column

---

### Computing checksum
1. Treat UDP segment as a sequence of `16-bit` integers.
2. Apply binary addition on every 16-bit integer
3. Carry if any from the most significant bit and add to the result
4. Compute 1’s complement to get UDP checksum

![[checksum.png| -m | -center]]

---

# Principles of reliable data transfer

>[!note] Transport layer
> ==Transport layer== resides on *end hosts* and provides *process-to-process* communication.

>[!note] Network layer
> ==Network layer== provides *host-to-host*, *best-effort* and *unreliable* communication.

## Reliable transfer over unreliable channel

```start-multi-column
ID: ID_f1av
Number of Columns: 2
Largest Column: standard
Shadow: off
Border: off
```
### Underlying network
- corrupt packets
- drop packets
- re-order packets
- deliver packets after an arbitrarily long delay

--- column-end ---
### End-to-end reliable transport service
- Guarantee packets delivery and correctness
- Deliver packets to receiver application in the same order they are sent

--- end-multi-column

>[!aside | right +++++]
>Characteristics of unreliable channel will determine the complexity of *reliable data transfer protocols* (==rdt==)

![[unreliablechannel.png| -m | -center]]

>[!note]
> ==Finite state machine== shows the $\frac{\text{event}}{\text{actions}}$ from one state to another.

## Reliable data transfer protocols

This will be illustrated through iterating the following

| **rdt version** | **scenario**                                   | **features used**                                             |
| --------------- | ---------------------------------------------- | ------------------------------------------------------------- |
| 1.0             | No error/ perfect network layer                | Nothing                                                       |     
| 2.0             | Data bit error                                 | Checksum, ACK, NAK                                            |
| 2.1             | Data bit error / ACK/NAK bit error             | Checksum, ACK, NAK, sequence number                           |
| 2.2             | As above                                       | NAK free                                                      |
| 3.0             | data bit error/ ACK/NAK bit error/ packet loss | Checksum, ACK, NAK, sequence number, timeout/ re-transmission |

---

### rdt 1.0
- Assume underlying channel is perfectly reliable.

![[rdt1.png| -m | -center]]

---

### rdt 2.0
- Underlying channel may *flip bits in packets*

To ==detect== bit errors, *receivers* may use [[#UDP Checksum | checksum]].

To ==recover== from bit errors:
- ==Acknowledgements (ACK)== : *receiver* explicitly tells sender that packet received is OK
- ==Negative acknowledgments (NAKs)== : *receiver* explicitly tells sender that packet has errors → *sender* ==retransmits== packet on receipt of NAK.

>[!caution] Stop and wait protocol
>Sender sends one packet at a time, then waits for a receiver response.

![[rdt2.png| -m | -center]]

![[rdt2fsm.png| -s | -center]]

#### What if `ACK/NAK` is corrupted?
When `ACK/NAK` is corrupted, sender does not know what happened at the receiver. Sender will just retransmit when it receives corrupted `ACK/NAK`. However, this may cause duplicate packets which the receiver cannot identify.


```start-multi-column
ID: ID_bbnd
Number of Columns: 2
Largest Column: standard
Border: off
Shadow: off
```
#### Corrupted ACK

![[rdt2corruptedack.png| -center | -m]]

--- column-end ---

#### Corrupted NAK

![[rdt2corruptednak.png| -center | -m]]

--- end-multi-column

---

### rdt 2.1

- To handle duplicates, sender retransmits current packet if ACK/ NAK is garbled.
- Sender adds *sequence number* to each packet
- Receiver *discards* duplicate packet

![[rdt2.1.png| -m | -center]]

#### Sender FSM

![[fsmsender2.1.png| -m | -center]]

#### Receiver FSM

![[fsmreceiver2.1.png| -m | -center]]

---

### rdt 2.2
>[!note]
>rdt 2.2 is a ==NAK-free== protocol

This is similar to [[Transport Layer#rdt 2.1 | rdt 2.1]] but *uses ACKs only*.

Instead of sending NAK, receiver sends ACK for the last packet received OK. *Receiver* explicitly include ==sequence number== of the packet being ACKed.

If there are duplicate ACKs at sender, sender retransmits the current packet.

![[rdt2.2.png| -m | -center]]

---

### rdt 3.0

>[!caution] Assumptions
>The underlying channel may:
> - flip bits in packets
> - lose packets
> - incur arbitrarily long packet delay
> - not re-order packets

==To handle packet loss==, sender waits *reasonable* amount of time for ACK. Sender *retransmits* if no ACK is received till ==timeout==.

Re-transmission will generate duplicate in some cases but receiver may use ==sequence number== to detect → receiver must specify the ==sequence number== of the packet being ACKed.

![[rdt2.2senderpktloss.png| -m | -center]]

![[rdt2.2receiverpktloss.png| -m | -center]]

![[fsmrdt2.2.png| -m | -center]]

---

## Performance of rdt 3.0

The performance of [[Transport Layer#rdt 3.0 | rdt 3.0]] is measured by its *utilisation*, $U_{\textsf{sender}}$, which is the fraction of time sender is busy sending.

Consider a packet size of $8000 \space \textsf{bits}$ and link rate = $1$ Gbps

$$
d_{\textsf{trans}} = \frac{L}{R} = \frac{80000}{10^9} = 0.008 \textsf{ msec}
$$

If RTT = 30 msec,

$$
\textsf{throughput} = \frac{L}{RTT + d+{trans}} = \frac{8000}{30.008} = 267 \textsf{ kbps}
$$

$$
U_{sender} = \frac{d_{trans}}{RTT + d_{trans}} = \frac{0.008}{30 + 0.008} = 0.00027
$$

---

## Pipelining
>[!note] The idea
> Send out the subsequent packet before ACK arrives

==Pipelining== allows sender to send multiple *in-flight*, yet to be acknowledged packets.

The main reason for pipelining is to increase *utilisation* of the sender.

Consequently, range of sequence numbers must be increased and there needs to be *buffering* at sender and/or receiver.

### Go-Back-N (GBN)

>[!note]
>In GBN, sender controls the flow of the packets.

The sender has a sliding window of size *N*, denoting the sequence of packets to send. Suppose there are 2 pointers, `send_base` and `nextseqnum`. While there are packets to send and `send_base + N < nextseqnum`, sender will send the packets pointed by `nextseqnum` and increments by 1.

`send_base` is incremented when there is an acknowledgment received from the receiver. Reception of duplicate ACKs does not trigger any mechanism.

There is a *single* timer which measures for ==timeout at the `send_base` packet==. Therefore, when there is a timeout, sender resends *all* the packets in the window, starting from `send_base`.

```plain-text
Function Sender {
	send_base = 0
	nextseqnum = 0

	while True {
		if nextseqnum < send_base + n {
			send packets[nextseqnum]
			nextseqnum += 1
		}

		if receive ACK {
			send_base += 1
			if send_base == nextseqnum {
				stop timer
			} else {
				start timer
			}
		}

		if timeout {
			start timer
			send packets[send_base]
			...
			send packets[nextseqnum - 1]
		}
	}
}
```


The ==Receiver== only keep tracks of the ACK packets that arrive in order and the `nextseqnum`. There is ==no *receiver buffer*== therefore, out-of-order packets and corrupted packets are discarded. It always send the acknowledgment of *last* in-order packet received upon reception of a new packet (successfully or unsuccessfully). As a result, it will generate acknowledgment messages if something goes wrong.

GBN adopts ==cumulative acknowledgments==. Receiving packet `N` means the packets `N-1`, `N-2, ...` are acknowledged as well.

```plain-text
function Receiver {
	nextseqnum = 0

	while True {
		if packet received {
			if not corrupted and seq_number = nextseqnum {
				deliver data to upper layer
				send ACK nextseqnum
				nextseqnum += 1
			} else {
				send ACK nextseqnum - 1
			}
		}
	}
}
```

![[gbn.png| -m | -center]]

### Selective repeat

>[!note]
>Selective repeat introduces *receiver buffer* to buffer out-of-order packets, as needed, for eventual in-order delivery to upper layer.

Receiver *individually acknowledges* all correctly received packets and buffers out-of-order packets, as needed, for eventual in-order delivery to upper layer

Sender maintains *timer* for each unACK’ed packet. When timer expires, retransmit only that unACK’ed packet

```start-multi-column
ID: ID_wn7q
Number of Columns: 2
Largest Column: standard
Shadow: off
Border: off
```

#### Sender
```plain-text
if next available seqnum in window {
	send packet
}

if timeout n {
	resend packet n
	restart timer
}

ack(n) in [send_base, send_base + N] {
	mark packet n as received
	if n is smallest unACKed packet {
		advance window base to next unACKed seq num
	}
}
```

--- column-end ---

#### Receiver

```plain-text
pkt(n) in [send_base, send_base + N] {
	send ACK(n)
	if out-of-order {
		buffer(n)
	} else {
		deliver
		else advance window to next not yet received pkt
	}
}

pkt(n) in [rcvbas - N, rcvbase - 1] {
	ACK(n)
}

otherwise {
	ignore
}
```


--- end-multi-column


<center><iframe width="650" height="500" src="https://www.baeldung.com/cs/selective-repeat-protocol"></iframe></center>

---

# TCP

>[!note]
>TCP is a connection-oriented transport which is complex in comparison to UDP and there are many variants.

### Features of TCP
- **Point-to-point** : one sender, one receiver
- **Connection-oriented** : handshaking (exchange of control message) before sending app data
- **Full duplex service** : bi-directional flow in the same connection
- **Reliable, in-order byte stream** : use sequence number to label bytes

---

A TCP connection is identified by 4 tuple: `(srcIPAddr, srcPort, destIPAddr, destPort)`
- Receiver uses ==ALL== four values to direct a segment to the appropriate socket.

TCP sends and receives *buffers*, where 2 buffers are created after handshaking at any side.

![[tcpbuffer.png| -m | -center]]

## TCP header

![[tcpheader.png| -m | -center]]

### TCP sequence number

The sequence number is the *byte number* of the ==first== byte of data in a segment.

For example, if I have a file of 500000 bytes and maximum segment size (MSS) is 1000 bytes → there will be 500 segments
>[!caution]
>MSS does not include the size of the header


Then the 1st data segment will contain byte 0 to 999 and so on.

Therefore, the sequence number of 1st TCP segment is `0`, 2nd TCP segment is `1000`, 3rd TCP segment is `2000` and so on.

### TCP Ack number

The ACK number is the sequence number of the *next* byte of data expected by the receiver

![[tcpseqnum.png| -m | -center]]

![[tcpevents.png| -m | -center]]

---

## TCP timeout

>[!note] How does TCP set appropriate timeout value?
>
>Too short: premature timeout and unnecessary retransmission
>
>Too long: slow reaction to segment loss/ resending packet loss

Therefore, timeout interval must be larger than RTT
>[!aside | right +++++]
>Timeout value is dynamic. It changes based on bandwith. The value of $\alpha$ is based on simulation.

TCP computes and *keeps updating* timeout interval based on estimated RTT. Fast retransmission allows to resend segments even before time expires.

$$
\textsf{EstimatedRTT} = (1 - \alpha) * \textsf{EstimatedRTT} + \alpha * \textsf{SampleRTT}
$$

$$
\textsf{DevRTT} = (1 - \beta) * \textsf{DevRTT} + \beta * | \textsf{SampleRTT} - \textsf{EstimatedRTT} |
$$

$$
\textsf{TimeoutInterval} = \textsf{EstimatedRTT} + 4 * \textsf{DevRTT}
$$

---

## Establishing connection

Before exchanging app data, TCP sender and receiver *shake hands* — sender and receiver agrees on connection and exchange connection parameters.

>[!caution]
>First 2 packets are reserved for TCP to exchange connection parameters. Only the *third* packet onwards will have data.



![[tcphandshake.png| -m | -center]]

### Closing connection

Client, server each close their side of connection and send TCP segment with `FIN` bit = 1

![[tcpcloseconnection.png| -m | -center]]