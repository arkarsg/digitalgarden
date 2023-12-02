#### Question 1

Consider two hosts, A and B, connected by a single link of rate $R$ bps. Suppose that the two hosts are separated by $m$ meters, and suppose the propagation speed along the link is $s$ meters/sec. Host A is to send a packet of size $L$ bits to Host B.

>[!info]- Delays
>>![[Introduction to Computer Networks#Delay, Loss, Throughput]]

##### a. Propagation delay

Propagation delay = $\frac{m}{s}$

##### b. Transmission delay

Transmission delay = $\frac{L}{R}$

##### c. End-to-end delay

End-to-end delay = $\frac{m}{s} + \frac{L}{R}$

##### d.

At `t = d_trans`, the last bit of packet just leaves A

##### e.

At `t = d_trans`, the first bit of packet is between A and B.

##### f.

At `t = d_trans`, the first bit of packet is at B 

##### g.

![[tut01q1g.jpeg|50%]]

>[!caution]
>It’s actually `0.0536 m`. Note that the question is `56 kbps`.

---

#### Question 2

![[IMG_93E204C2121D-1.jpeg | -m | -center]]

>[!caution]
>Be careful of bytes and bits. Do the necessary conversions



---

#### Question 3

![[IMG_71BD76747656-1.jpeg | -m | -center]]

Reasons to use message segmentation:
- If a bit is corrupted, only the affected packet is dropped. Without message segmentation, the entire file have to be resent.
- May take up the entire queue and cause delays for other packets

Drawbacks of message segmentation:
- Destination has to receive the packets in the correct order
- Since the packet size is constant, header size for packets may be larger

---

#### Question 4

Minimum number of links between $N$ devices:
- Consider a tree-like structure → $N-1$ links

Pros:
- No need for long bandwidth cables


Cons:
- Greater end-to-end delay
- *single point of failure*

---

Maximum number of links between $N$ devices:
- Each link is connected to each other → $N\choose{2}$ links
- *known as mesh structure*

Pros:
- Lower end-to-end delay
- *Robust, no single point of failure*

Cons:
- Need longer physical media
- More expensive

---
