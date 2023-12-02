>[!quote] DNS (RFC 1034, 1035)
>DNS stands for ==Domain Name System==. It is part of the [[Application Layer]].

>[!aside | right +++++]
> IP address is a *32-bit integer* divided into *4* segments.
> 
> The mapping between hostname and IP address *may not be* one-to-one for many reasons, such as load balancing purposes.


There are *2* ways to identify a ==host==.
- ==Hostname==: `www.example.org`
- ==IP address==: `93.184.216.34`


>[!note]
>DNS translates between the two. A ==client== must carry out the DNS query to determine the IP address corresponding to the server name prior to the connection.

---

## Resource records

Mapping between hostnames and IP addresses are stored as ==resource records== (RRs), and has the following formal:

>[!aside | right +++++]
>Note that there are also other types not covered.


| **Name**   | **Value**                                            | **Type** | **TTL** |
| ---------- | ---------------------------------------------------- | -------- | ------- |
| hostname   | IP address                                           | A        |         |
| alias name | Canoncical name                                      | CNAME    |         |
| domain     | Hostname of authoritative name server of this domain | NS       |         |
| name       | Name of mail server associated with `name`           | MX       |         |

>[!aside | right +++++]
> ==Time to live (TTL)== is the time before local server removes the cached lookup


>[!note] Authoritative name server
>There are `www.nus.edu.sg` and `luminus.nus.edu.sg`. Then, what is the server that has the authority to respond to the request?
>
>This server is known as the ==authoritative name server==.

---

## Distributed, hierarchal database

DNS stores RR in *distributed* databases implemented in ==hierarchy== of many name servers.

>[!note]- Why distributed?
>Note that there are billions of devices connected in the internet. Therefore, all DNS records should not be recorded in one DNS server for availability.

![[DNSheirarchy.png|80%]]

### Root servers

Root servers answers requests for records in the root zone by returning a list of ==authoritative name servers== for the appropriate ==top-level domain (TLD)==.

>[!note] Top-level domain (TLD)
>TLD is responsible for `.com`, `.net`, `.edu` and all top-level country domains `.uk`, `.sg`, `.jp`

>[!note] Authoritative servers
>Authoritative servers are organization’s own DNS server(s), providing authoritative hostname to IP mappings for organization’s named hosts such as web or mail.
>
>This can be maintained by organization or service provider.


### Local DNS server

>[!aside | right +++++]
>This removes the need to contact the root server every time. If retrieved from local DNS server, the answer is ==non-authoritative answer==.

Local DNS servers do not strictly belong to hierarchy. Each ISP has a local DNS server also called the *default name server*.

When a host makes a DNS query, query is sent to its local DNS server to:
1. retrieve name-to-address translation from local cache
2. local DNS server acts as proxy and forwards query into hierarchy if answer is not found locally

#### DNS Caching

Once a name server leans mapping, it *caches* the mapping. This is ==best-effort== name-to-address translation as cached entries may be out of date.

Cached entries also expire after some time known as ==TTL==. As such, if a name host *changes* its IP address, it will not be known internet-wide until all TTLs expire.


```start-multi-column
ID: ID_1h6f
Number of Columns: 2
Largest Column: standard
Shadow: off
Border: off
```

### Iterative query

![[iterativequery.png|100%]]

--- column-end ---

### Recursive query

![[recursivequery.png|100%]]

--- end-multi-column

>[!caution]
>DNS runs over [[Application Layer#UDP service | UDP]].
>
>Although UDP is not reliable, multiple UDP is issued back to back so when there is packet loss, it is not a big issue. It is also fast as there is no need to incur RTT to establish a connection. DNS query can be sent quickly. Most of the query is sent to local server. So the communication is within the network and the chance of being dropped or corrupted is very low.

---

# Socket programming

>[!note] Process
>A process is a program running within a host. Within the same host, two processes communicate using *inter-process communication* defined by OS.
>
>Processes in different hosts communicate by exchanging ==messages== according to [[Introduction to Computer Networks#Protocol | protocols]].

## Addressing process

Note that hosts can be identified by its IP address.

>[!aside | right +++++]
>IP address alone is not sufficient to identify a process as there may be processes running concurrently within a host.

A process can be identified by ==IP address and port number==.

### Port number
A port number is *16-bit* integer with 1 - 1023 reserved for standard use. HTTP server uses port number `80` and SMTP server uses port number `25`.

With the port number, packet received by the host through its IP address can be dispatched to the *right process* in the host using the port number of the process.

---

## Sockets
>[!note] Definition of sockets
>Socket is the software interface between ==app processes== and ==transport layer protocols==.
>
>Processes sends/ receives messages to/ from its sockets.

There are *2* types of sockets: TCP and UDP sockets

>[!caution] Key differences
>In TCP, two processes communicate *as if there is a pipe between them*. The pipe *remains in place* until one of two processes closes it. When one of the process wants to send more bytes to the other process, it simply *writes data to that pipe*. The sending process does not need to attach a destination IP address and port number to the bytes in each sending attempt as there is a logical pipe.
>
>In UDP, there is a need to form *UDP datagram* packets explicitly and attach destination IP address/ port number to every packet.

>[!aside | right +++++]
>You can run UDP and TCP concurrently for the same port number.

Applications (or processes) treat the internet as a black box, sending and receiving messages through sockets.

```start-multi-column
ID: ID_zr80
Number of Columns: 2
Largest Column: standard
Shadow: off
Border: off
```

### TCP Socket
Reliable, byte stream-oriented socket
- When contacted by client, server TCP creates new socket.
- Server uses IP and port number to distinguish clients.
- Ensures that packet received from each client is not corrupted or lost.

--- column-end ---

### UDP Socket
Unreliable datagram socket
- Server uses one socket to serve all clients
- No connection is established before sending data
- Sender needs to explicitly attach destination IP address and port number to ==each packet==.
- Transmitted data may be lost or received out of order

--- end-multi-column

>[!aside | right +++++]
>You can configure how many TCP sockets a server side can have. OS may have a limit as it needs to allocate resources.

---

# Socket programming with UDP


```start-multi-column
ID: ID_2vxl
Number of Columns: 2
Largest Column: standard
Border: off
Shadow: off
```

### Server
Application program explicitly attaches ==IP address== and port number to ==each packet==.

```python
from socket import *

serverPort = 2105

serverSocket = socket(AF_INET, SOCK_DGRAM) # IPv4, UDP socket

# bind socket to local port number 2105
serverSocket.bind( ('', serverPort) )
print("🚀 Server is ready to receive message")

# extract client address from received packet
message, clientAddress = serverSocket.recvfrom(2048) # receive datagram buffer size

# echo
serverSocet.sendTo(message, clientAddress)

serverSocket.close()
```

--- column-end ---

### Client
Extracts sender IP address and port number from the received packet

```python

from socket import *

serverName = 'localhost' # client and server on the same host
serverPort = 2105

clientSocket = socket(AF_INET, SOCK_DGRAM)

message = "Message from client"

clientSocket.sendTo(message.encode(), (serverName, serverPort))

receivedMessage, serverAddress = clientSocket.recvfrom(2048)

print("From server: ", receivedMessage.decode())

clientSocket.close()
```


--- end-multi-column



# Socket programming with TCP

Before *client* sends the first packet, it attempts to establish a TCP connection to the *server* first.

When contacted by the client, *server TCP* creates a ==new socket== for server process to communicate with that client → This allows the server to talk to multiple clients individually.


```start-multi-column
ID: ID_vktw
Number of Columns: 2
Largest Column: standard
Border: off
Shadow: off
```

### Server
```python
from socket import *

serverPort = 2105
serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(('', serverPort))
serverSocket.listen() # listen for incoming TCP request
print("🚀 Server is ready to receive message")

connectionSocket, clientAddr = serverSocket.accept() # returns a new socket to communicate with client socket
message = conncetionSocket.recv(2048)

connectionSocket.send(message)
connectionSocket.close()
```

--- column-end ---

### Client

```python
from socket import *

serverName = 'localhost'
serverPort = 2105

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect( (serverName, serverPort) ) # establish a connection

message = "Message from client"

clientSocket.send(message.encode())

receivedMessage = clientSocket.recv(2048)
print("From server: ", receivedMessage.decode())

clientSocket.close()
```

--- end-multi-column

---
