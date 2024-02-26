>[!note] Motivating example
>Suppose we have a file to transfer. We do not care about what kind of file is being transferred, as long it is transferred as bits and bytes — the data reaches reliably or data is transferred maximally.
>
>Now, we wish to transfer multimedia data

We define a *multimedia network application* as any network application that employs audio or video. This is in [[Application Layer]] and [[Transport Layer]].

# Streaming 
>[!note] OTT
>Multimedia is delivered as over-the-top (OTT) as they do not have a dedicated infrastructure, such as cables for the customer.

**Streaming** can begin *playout* before downloading entire file. The audio/ video is **stored** at server or CDNs. It can transmit faster than audio/ video will be rendered (which implies storing/ buffering at client)

**Conversational** is voice/video over **IP** which is an interactive nature of man-to-man conversation limits delay tolerance
- Delay more than *400ms* is considered intolerable

**Streaming live** audio, video is typically done with CDNs and has a threshold of *10s*

---

# Video
>[!info] Video
>Video is a sequence of images displayed at constant rate of 30 images / seconds. A digital image is an array of pixels and each pixel is represented by bits.

Video has a *high bit rate*. To reduce data usage, we compress the video.

### Spatial coding
Exploiting redundancy *within* the image. For example, instead of sending $N$ values of same color, send only two values *color* and number of repeated values $N$.

### Temporal coding
Instead of sending complete frame at $i + 1$, we only send the differences between $i$ and $i + 1$

## Encoding
### Constant bit rate
Video encoding rate is fixed. Therefore, need to set your bitrate relatively high to handle more complex segments of vide. The consistency of CBR makes it well-suited for real-time encoding
### Variable bit rate
Video encoding rate changes as amount of spatial and temporal coding changes.

>[!example]
>MPEG, 1.5Mbps
>MPEG4, H.264
>H.265, 10Mbps

## Stored video
![[multimedia-storedvideo.png|50%]]

Note that at the time the first chunk of the video is played, the last few parts of the video is being sent

### Continuous playout constraint
Once client playout begins, playback must match original timing, but network delays are variable (*jitter*). Other challenges include client interactivity such as pause, fast-forward, rewind and jump through video.

Video packets may be lost which are retransmitted. Therefore, the client payout delay needs to be adjusted so that the client payout is *always* on the right of client-video reception.

![[multimedia-playout.png|50%]]

#### Client side buffering and playout delay
Compensate for network-added delay, delay jitter.

Suppose we have constant bit rate $r$ and variable fill rate $x(t)$ and buffer fill level $Q(t)$.
1. Initial fill of buffer until playout beings at $t_p$
2. Playout begins at $t_p$
3. Buffer fill level varies over time as fill rate $x(t)$ varies and playout rate $r$ is constant

- If average fill rate is less than $r$, buffer eventually empties (causing freezing of video playout until buffer again fills)
- average fill rate more than $r$, buffer will not empty provided initial playout delay is large enough to absorb variability in $x(t)$

>[!example]
>Suppose we have a playout buffer of size $B_\text{playout} = 8 \text{MB}$
>
>- The buffer is initially empty. The time when you press play is $t_0$. It takes 4 seconds to fill the buffer $B$ to its mid-point (4 MB of data)
>- At that point $t_0 + 4$ seconds, the media player starts to play the video.
>- The video has a size of $14$ MB
>- The data continues to arrive after $t_0 + 4$ seconds from the server at a constant rate of $8$ Mb/s and the player decodes the media at a rate of $4$ Mb/s until the video ends.
>
>Rate of buffer growth = fill rate - playout rate = 4 Mbps. Now let this be the chunk per second.
>Therefore, the video will have 28 chunks, buffer will have 16 chunks and buffer fill level $Q(t_0 + 4)$ is 8 chunks.
>
>To fill the buffer, with buffer growth rate of 1 chunk per second, the time taken by the buffer to fill is
>$$ (t_0 + 4) + \frac{16-8}{1} = t_0 + 12$$
>
>At $t_0 + 12$, video is played till $(t_0 + 12) - (t_0 + 4) = 8$ chunks
>At $t_0 + 12$, data is delivered till, 8 + 16 = 24 chunks
>Fill rate after $t_0 + 12$, $\bar{x}$ = 1 chunk per sec (playout rate)

## Streaming multimedia

### UDP
- Server sends at rate appropriate for client and often, send rate = encoding rate = constant rate.
- *Push based* streaming

UDP has no congestion control. Hence transmission is done without rate control restriction. Short playout delay (2 - 5s) to remove network jitter.

**Error recovery** : Done at application-level.

Video chunks are encapsulated using RTP (Real time transport protocol). This includes:

| Seq num | Time stamp |   video encoding  | 
| ------- | ---------- | --- |

Control connection is maintained *separately* using **RTSP** (real time streaming protocol)
- Used for establishing and controlling media sessions between endpoints
- Clients issue commands such as *play, pause, record*

**Drawbacks**
- Need for a separate media control server like RTSP which is complex and costly
- UDP may *not* go through firewalls

### HTTP
Multimedia file is received via HTTP GET. This is known as a client pull-based streaming.

![[multimedia-buffer.png|80%]]


```start-multi-column
ID: ID_40va
Number of Columns: 2
Largest Column: standard
Border: off
Shadow: off
```

#### Advantages
- HTTP/ TCP passes more easily through *firewalls*
- Network infrastructure like CDNs and routers fine tuned for HTTP/TCP


--- column-end ---

#### Drawbacks
- Fill rate fluctuated due to TCP congestion control and retransmission (in-order delivery)
- *Larger* playout delay; smooth TCP delivery rate

--- end-multi-column

![[multimedia-http.png|80%]]

---

# Voice-over-IP
VoIP need to maintain an *end-to-end delay* for a conversational aspect. Higher delays are noticeable and impairs interactivity: *400 ms*

This includes application-level (packetization, playout, network delays). And, data loss over 10% makes conversation unintelligible.

### Challenge
- No upper bound on *delay*
- No upper bound on percentage of *packet loss*

## Speaker
Speaker alternate talk spurts and silent periods. Packets are generated only during *talk spurts*. This is $20ms$ chunks at $8KB/s$.

- Application layer header added to chunk
- Chunk + header encapsulated into UDP or TCP segment — application sends segment into socket every 20ms during talk spurt

## Loss and delays

### Network loss
IP datagram lost due to network congestion (router buffer overflow)
### Delay loss
IP datagram arrives too late for playout at the receiver. VoIP applications typically use UDP to avoid congestion control.
### Loss tolerance
Depending on voice encoding, loss concealment, packet loss rates between 1% and 10% can be tolerated

![[Screenshot 2023-11-19 at 5.20.53 PM.png|80%]]

## Fixed playout delay
Receiver attempts to playout each chunk exactly $q$ ms after chunk was generated.
- Chunk has time stamp $t$: Play out chunk at $t + q$
- Chunk arrives after $t + q$: data arrives too late for playout → data lost

>[!caution]
>No value of $q$ can guarantee an optimal performance

## Adaptive playout delay
**Goal** : low playout delay, low late loss rate
**Approach** : adaptive playout delay adjustment

- *Estimate* network delay, *adjust* playout delay at beginning of each talk spurt
- Silent periods *compressed* and *elongated*, chunks are still played out every 20ms during talk spurt

![[multimedia-adaptiveplayoutdelay.png|50%]]

### Adapting the value of $q$

### Recovery from packet loss
#### **Forward Error Correction (FEC) **
- send enough bits to allow recovery without retransmission  

For every group of $n$ chunks,
- Create redundant chunk by XOR-ing $n$ original chunks
- Send $n+1$ chunks

#### **Piggyback**
Send lower resolution audio stream as redundant information
![[multimedia-piggyback.png|50%]]

#### Interleaving to conceal loss
Audio chunks divided into smaller units ie four 5ms units per 20ms audio chunk. Packet contains small units from *different* chunks.

If packet is lost, still have *most* of every original chunk → no redundancy overhead, but increases playout delay, even without error.

---

# Dynamic adaptive streaming over HTTP (DASH)
>[!note]
>Used by YouTube (proprietary version) and Netflix

## HTTP Streaming
Simple HTTP streaming just GETs the whole video file from an HTTP server
### Drawbacks
- Can be wasteful, need large client buffer
- All client receive the same encoding of video, despite the variation in device/ network bandwidth
---
## How it works
- Data is encoded into different qualities and cut into short segments
- Clients first downloads *manifest* files, which describes the available videos and qualities
- Client/ player executes *adaptive bitrate algorithm* to determine which segment to download next

```start-multi-column
ID: ID_npuj
Number of Columns: 2
Largest Column: standard
Border: off
Shadow: off
```

#### Server
- Divides video into multiple chunks
- Each chunk stored/ encoded at different rates
- *Manifest file* : provides URLs for different encoding

--- column-end ---

#### Client
- Periodically measures server-to-link bandwidth
- Consulting manifest, one chunk at a time
- Chooses encoding sustainable with the given current bandwidth
- Can choose different coding rates at different points in time (depending on available bandwidth at time)

--- end-multi-column

## Intelligence at “client” 
- *when* to request chunk (so that buffer starvation, or overflow does not occur)  
- *what* encoding rate to request (higher quality when more bandwidth available)  
- *where* to request chunk (can request from URL server that is “close” to client or has high available bandwidth)

---

# Content Distribution Network
Store and serve multiple copies of videos at geographically distributed sites

>[!example]
>CDN : stores copies of content at CDN nodes
>Client requests content — service provider returns manifest
>Using manifest, client retrieves content at highest supportable rate
>May choose different rate or copy if network path is congested

---
# Audio
## Analog audio signal
CD : 44100 samples/ second

Each sample is quantized/ rounded and each quantized value is represented by bits for example 8bits → 256 quantized values → 64000bps. Receiver converts bits back to analog signal (DAC) with some quality reduction.

---


