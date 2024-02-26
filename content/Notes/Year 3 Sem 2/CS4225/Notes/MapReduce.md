# Typical Big Data Problem
- Iterate over a large number of records
- Extract something of interest from each
- Shuffle and sort intermediate results
- Aggregate intermediate results
- Generate final output

**Map** : Extract something of interest from each
**Reduce** : Aggregate intermediate results

>[!example] Tabulating election results form multiple polling sites
> Multiple voting stations (multiple chunks) 
>- Need to aggregate vote counts from the voting stations
>
>**Map**
> - Map output : `party:count` value
> 
> **Shuffle**
> - Collect the outputs from `map` results
> - Sort
> 
> **Reduce**
> - Sum the counts
> 
> ![map-reduce-voting|500](Screenshot%202024-02-04%20at%204.08.02%20PM.png)

Therefore, the programmer needs to specify the *map* function and *reduce* function
- $map(k_1, v_1) → List(k_2, v_2)$
- $reduce(k_2, List(v_2)) → List(k_3, v_3)$
	- All values with the same key are sent to the same reducer

![map-reduce-implementation|500](Screenshot%202024-02-12%20at%201.19.47%20PM.png)

>[!note] 4: Why `map` writer writes to local hard disk? Why not write to other machines?
>- Writing to main mem is less reliable than writing to hard disk
>	- Data on hard disk is persistent even if there is a failure
>- Capacity of the hard disk is larger than the capacity of the main mem
>- The bandwidth of network is limited and writing to other machines incurs bandwidth cost

>[!note] 6: Reduce `write` can be local write or remote write to other machines
>Output file will go to a distributed file system
---
## Runtime
- Handles scheduling : Assigns workers (containers) to map and reduce tasks
- Handles data distribution : Moves processes to data
- Handles synchronization : Gather, sorts and shuffles intermediate data
- Handles errors and faults : Detects worker failures and restarts
---
## Partition by hash

---
## Combiners
- Combiners *locally* aggregates output from mappers
- Combiners may be *mini-reducers*

![combiners|500](Screenshot%202024-02-12%20at%201.26.06%20PM.png)

### Correctness of Combiner
- Combiner does not affect the correctness of the final output, whether the combiner runs 0, 1 or multiple times

**In general**, it is correct to use *reducers as combiners* if the reduction involves a binary operation that is both
- **Associative** : $a + (b + c) = (a + b) + c$
- **Commutative**: $a + b = b + a$

---
# Hadoop File System

**In the past**
- Compute nodes have very small local disks but very good CPU → suitable for compute
- Storage nodes have very weak CPU and rich disk → suitable for storage
![legacy|500](Screenshot%202024-02-12%20at%201.33.00%20PM.png)

This is meant for tasks that are computationally expensive:
- Small input data
- Expensive simulation and a lot of computation

**Today**
Tasks today involves a lot of data but is not computationally expensive
- Example: video streaming

Therefore, the above architecture is no longer suitable → combine the compute and storage

>[!note] Don’t move data to workers, move processing to the data

## Assumptions
- **Commodity hardware instead of *exotic* hardware**
	- Scale *out*, not *up*
- **High component failure rates**
	- Inexpensive commodity components fail all the time
	- Failures are not an exception — can be hardware or software
	- Many tasks and machines → a lot of possible software and hardware failures
- ***Modest* number of huge files**
	- Number of files and size of files
	- *Huge* : Scale of 1000GB or more
	- Example : 10 files in the petabytes range
- **Files are write-once, mostly appended to**
- **Large streaming reads instead of random access**
	- Sequential access over random access
	- High sustained throughput over low latency

## Design decisions
- **Files stored as chunks (split)**
	- Fixed size (64MB for GFS and 128MB for HDFS)
	- Utilise the bandwidth of the hard disk
- **Reliability through replication**
	- Each chunk replicated across 3+ chunkservers
	- For each data, there are 2 other copies in the cluster
	- Can tolerate up to 2 failures
	- Why not more? Storage overhead and synchronisation, wastes a lot of IO
	- Why more? Better IO, flexibility of scheduling, more reliable
- **Single master to coordinate access, keep metadata**
	- Simple centralised management

---
# HDFS architecture
![hdfs-architecture|500](Screenshot%202024-02-12%20at%201.49.29%20PM.png)

**HDFS namenode** does not store the actual data. There is only $1$ namenode It only stores the *information* about the data:
- Number of chunks
- Location of each chunk
- Replication
- space managemen

**Actual** data is stored in the **datanode**. There can be $n$ datanodes.

**Maintaining overall health**:
- Periodic communication with the datanodes
- Block re-replication and re-balancing
- Garbage collection

>[!example] Read
>1. *Client* sends path to the *namenode*
>2. *namenode* sends the location back to the *client*.
>3. Given the location, *client* reads from the datanode
>4. *Datanode* responds with the data to the *client*

>[!caution] Actual data never passed through the namenode
>Actual read and write only happens in the datanode

>[!note] Replication on write
>*Namenode* decides which datanodes are to be used as replicas. The 1st datanode forwards data blocks to the 1st replica, which forwards them to the 2nd replica, and so on.

>[!note] Lost namenode’s data
>All files on the FS cannot be retrieved since there is no way to reconstruct them from the raw block data. Hadoop provides 2 ways of backup : through backups (replication) and secondary namenodes

![all-nodes|500](Screenshot%202024-02-12%20at%201.58.47%20PM.png)

*namenode* and *job submission node* can be on the ==same physical machine== or on ==different machines==

----