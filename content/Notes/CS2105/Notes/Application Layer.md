#notes #cs2105
>[!note] Application layer defines…
>communication behaviour of network applications.

![[applicationlayer.png| -m | -center]]

# Principles of network applications

## Creating network applications

%% to find out more examples of network applications %%

==Network applications== are programs that run on *different* hosts and communicate over network. For example, web server software → browser software.

==Classic structures== of network applications:
- Client-server
- Peer-to-peer (P2P)

---

## Client-Server architecture
![[clientservermodel.png| -xs | -center]]

```start-multi-column
ID: ID_b2x6
Number of Columns: 2
Largest Column: standard
Border: off
Shadow: off
```

### Server
==Server== offering certain services – for example, web server stores webpages, email servers provides email services.
- Waits for incoming requests
- Provides requested service to client
- data centers for scaling

--- column-end ---

### Client

==Client== requests services from ==server==.
- Initiates contact with server
- *Typically* requests service from server
- For *web*, client is usually implemented in browser.

--- end-multi-column

## P2P architecture
![[Screenshot 2023-08-19 at 11.37.05 PM.png | -xs | -center]]
In ==P2P== architecture, data is downloaded from other *users* and is uploaded simultaneously for other *users*. In this architecture, there is no dedicated user.
- Not always-on server
- Arbitrary end systems directly communicate
- Peer requests services from other peers, provide service in return to other peers
	- ==Self-scalable==: new peers bring new service capacity, as well as new service demands
- Peers are intermittently connected and change IP addresses
	- complex management

## Common requirements

![[requirementsexample.png| -s | -center]]
```start-multi-column
ID: ID_jh8g
Number of Columns: 2
Largest Column: standard
Shadow: off
Border: off
```

### Data integrity

Observe that some applications require 100% reliable data transfer, such as web transactions or file transfer. Hence, tolerance for packet loss is low and require re-transmission.

However, some applications such as video streaming can tolerate some data loss.


--- column-end ---

### [[Introduction to Computer Networks#Throughput | Throughput]]
Some applications require minimum amount of bandwidth to be *effective*, such as video on-demand.

Some applications make use of whatever *throughput* available.

--- end-multi-column


```start-multi-column
ID: ID_6bk9
Number of Columns: 2
Largest Column: standard
Shadow: off
Border: off
```

### Timing
Some applications require low delay to be *effective*


--- column-end ---

### Security
Encryption, data integrity and authentication


--- end-multi-column

---

>[!caution] App-layer protocols ride on transport layer protocols:
>
>TCP and UDP to handle low level implementations such as how data is transferred.


```start-multi-column
ID: ID_mhd1
Number of Columns: 2
Largest Column: standard
Shadow: off
Border: off
```

### [[Transport Layer#TCP]]

- reliable data transfer – will ==re-transmit== when data is lost or corrupted
- flow control – sender will not overwhelm receiver
- congestion control – throttles sender when network is overloaded
- does not provide timing, minimum throughput guarantee, security

--- column-end ---

### [[Transport Layer#UDP]]

- unreliable data transfer – for multi-media, will not re-transmit, fast transmission is more important than packet loss
- no flow control
- no congestion control
- does not provide timing, minimum throughput guarantee, security

--- end-multi-column

---



