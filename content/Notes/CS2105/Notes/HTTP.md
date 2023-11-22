#notes #cs2105 
>[!caution] HTTP
> ==Hypertext Transfer Protocol== is an example of [[Application Layer | application protocol]] for the web.

>[!note] Some basics
>Web supports many kinds of applications. A *web page* is resource downloaded from a server which consists of a *base HTML file* and referenced objects such as *image, audio, scrips, animations…*
>
>Each object can be addressed by a *URL*. Retrieval/ download of objects are done *sequentially*.

---

HTTP uses a [[Application Layer#Client-Server architecture | client-server architecture]] where:
- ==client==: usually a browser that requests, receives and displays web objects
- ==server==: web server sends objects in response to requests

---

HTTP runs over [[Transport Layer#TCP | TCP]] as transport service.
1. Client *initiates* TCP connection to server
2. Server *accepts* TCP connection request from client
3. HTTP messages are exchanged between client (web browser) and HTTP server (web server) over TCP connection
4. TCP connection is closed

---

## Types of HTTP connections

>[!aside | right +++++]
>The version of HTTP and pipelining is decided by client.



```start-multi-column
ID: ID_evh4
Number of Columns: 2
Largest Column: standard
Border: off
Shadow: off
```

### Non-persistent HTTP (HTTP 1.0)
- ==at most== one object sent over a TCP connection. The connection is then closed.
- Downloading multiple objects require multiple connections
- Before HTTP 1.1, browsers open *parallel* TCP connections — each TCP connection for each object

--- column-end ---

### Persistent HTTP (HTTP 1.1)
- ==multiple== objects can be sent over *single* TCP connection between client and server.
- ==Server== leaves connection open after sending response
- ==Client== may send multiple requests *back to back* – can be done in parallel → ==persistent with pipelining==


--- end-multi-column

>[!note] Non-persistent HTTP example
>1. HTTP client initiates TCP connection to HTTP server at *URL* port 80
>2. HTTP server at host *URL* is waiting for TCP connection and *accepts* connection
>3. HTTP client sends *requests messages* into the TCP socket
>4. HTTP server receives request message, *forms* response message containing the requested object and sends message to the client
>5. ==HTTP server== closes TCP connection
>6. HTTP client receives response message containing HTML file and displays HTML
>7. Repeat step 1 - 5 for all objects required in the HTML file

---

## Non-persistent HTTP

### **Response time** – Round trip time
==RTT== is the time for a packet to travel from client to server *and go back*
- 1x RTT to establish TCP connection
- 1x RTT for HTTP request and the first few bytes of HTTP response to return
- 1x file transmission time
![[rttsequence.png| -s | -center ]]

>[!caution]
>OS incurs overhead for every TCP connection.

---

## HTTP request messages

There are 2 types of HTTP messages: ==requests== and ==response==

>[!note] HTTP request message
> Line `1` refers to the *request* line with the *GET* method.
> 
> Line `2-3` are referred to as the *header lines*
> ```http
GET /index/html HTTP/1.1\r\n
Host: www.example.org\r\n
Connection: keep-alive\r\n
…
\r\n

![[requestmessage.png| -s |-centre]]

## HTTP response messages

>[!note] HTTP response message
>```http
>HTTP/1.1 200OK\r\n
>Date: Wed, 23 Jan, 2023

### HTTP response code
Status code appears in 1st line in server-to-client response message.

For example,

| **Code** | **Description**                         |
| ---- | ------------------------ |
| 200  | `OK` - Request succeeded |
| 301  | `Moved permanently`      |
| 403  | `Forbidden`              |
| 404  | `Not found`              |

---

## Cookies

>[!caution]
>HTTP is designed to be ==stateless==.
>
>Server maintains no information about past client requests.

However, there are some applications that require states to be maintained.

>[!note] Cookies
>Cookies are ==HTTP messages that carry state==.
>This is contained in the *cookie header field* of HTTP request and response message.
>Cookie file kept on user’s host, managed by user’s browser
>Back-end database at Web site.


![[cookiediagram.png | -center | -m]]

### Conditional GET

>[!note] Goal of Conditional GET
>Don’t send object if ==client== cache has up-to-date cached version of the object.

Therefore, in `cache`, specify the date of cached copy in HTTP request.

When the HTTP request is made, if the object is modified after `date`, HTTP response will have a `200 OK` code and sends the data from server. Otherwise, HTTP response will have `304 Not modified` and data will not be sent.

![[conditionalget.png| -s | -center]]

---

