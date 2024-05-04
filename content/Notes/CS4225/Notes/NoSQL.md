SQL databases are very reliable and stable. However, they are very expensive and cannot easily be scaled up.

For many applications, database may not be fully reliable. For example, it may not be consistent for a while. This is still suitable for many web applications. This is the motivation of ==NoSQL==.

---

# NoSQL
- Refers to a ==non-relational database==
	- Stores data in format other than relational tables
- SQL refers to traditional relational database management systems
	- NoSQL systems can involve SQL-like querying language in many cases

## Brief overview
- Horizontal scalability
- Replicate and distribute data over many servers
- Simple call interface, supports SQL, Python etc
- Weaker concurrency model than RDBMS
	- Not as reliable as traditional RDBMS
- Efficient use of distributed indexes and RAM
- Flexible schemas

---
## Key-Value stores
Each tuple is a key-value pair.
- `key` are usually primitives and can be queried
- `value` can have various datatypes – primitive or complex
	- Usually cannot be queried
	- `int`, `strings`, `lists`, `json`, `html`, `blob`

### API
`get` - fetch value associated with key
`put` - set value associated with key

>[!note]
>You can only do simple queries and *range queries*. You cannot query values

Suitable for:
- Small continuous read and writes
- Storing *basic* information or no clear schema
- When complex queries are not required

>[!example]
>- Storing user session
>- Caches
>- User data that is often processed individually
---
## Documents
Document store is similar to SQL database.

A database can have multiple **collections**.

A **collection** is made up of multiple **documents**.

### Document
- Is a JSON like object
- Has field and values
	- Different documents can have different fields
		- Allows new features to be added quickly without changing the schema
		- Newer documents will have fields while old documents will not
	- Can be nested

```json
[
	{
		_id: ...,
		item: "Canvas",
		qty: 100,
		size: {
			h: 20,
			w: 20
		}
	}
]
```

### Querying
Can query based on content of the document and CRUD operations

---

## Wide column store
Storing data column by column
- Related groups of columns are grouped as *column families*

![wide-column-example|500](Screenshot%202024-04-25%20at%209.39.56%20PM.png)

---

## Graph
Store data based on their connections
- Different nodes and links to represent the relationship
- May be directed
- Different link may have different definitions

---

## Vector databases
- Store vectors
	- Each row represents a point in $d$ dimensions
- Allow fast similarity search
	- Given a query, retrieve similar neighbours from the database

**Key features**
- Scalability
- Real time updates
- Replication

---

# Eventual consistency
>[!note] Strong consistency
>Any reads immediately after an update must give the same result on all observers
>
>- If node $A$ is performing a write on record $X$, node $B$ and node $C$ will block reading $X$. Readers are blocked until replication is complete.
>- This applies for distributed database.
>- To achieve strong consistency, performance is a tradeoff

>[!note] Eventual consistency
>If the system is functioning and we wait long enough, eventually, all reads will return the last written value
>
>- If node $A$ performs a write on document $X$ and node $B$ reads $X$, $B$ may read the old value. Eventually, newer read calls will be passed to $B$
>- Between write operation and transfer to node $B$, read operations on node $B$ will get outdated data.

Eventual consistency offers better availability at the cost of weaker consistency guarantees. Acceptable for most web applications but not financial transactions for example.

## BASE
>[!note]
>Relational database guarantees **ACID** guarantees

NoSQL generally relaxes to **BASE** approach
- **Basically available** : basic reading and writing operation available most of the time
- **Soft state** : the state of the data could change without application interactions due to eventual consistency
- **Eventually consistent** : Contrast to **strong consistency**

>[!note]
>Data stored for web applications such as user data, etc, consistency is not as critical as business operations. Availability is more important

Recent NoSQL systems are *configurable* consistency and can be configured for different consistency *including **strong***

>[!important] 
>ACID are strong constraints. By weakening these constraints to BASE, one can improve performance
---

# Duplication

In SQL RDBMS, we can easily perform `JOIN`

In NoSQL, it is difficult to execute `JOIN` as different documents have different fields.

==Duplication== solves this by duplicating a field into a document. This is also known as *denormalization*

However, changes in a collection needs to be reflected in the denormalized table.

>[!note] Why does this work?
>Storage is cheap, duplicate to improve efficiency
---
# Data Partitioning

## Table partitioning
- Put different collections or tables on different machines

## Horizontal partitioning
>[!note] Key idea
>Partition pruning saves a lot of work

Different tuples are stored in different nodes
- Also called *sharding*
- **Partition key** : is the variable used to decide which *node* each tuple will be stored on.
- Tuples with the same shard key will be on the same node

If the partition key is imbalanced, this cause lack of scalability.

==Range partition==
- Split partition key based on range of values

==Hash partition==
- Hash partition key then divide that into partitions based on range
	- Hash function causes the partition key to fall into a bucket.
	- A good hash function will spread out the keys equally

**Adding/ removing a node**
Inefficient to redo the hash function and redistribute the data around the whole cluster.
→ Consistent hashing

### Consistent hashing
- Output of the hash function is ==circular==
- Each node has a marker (or multiple markers per node)
- Each tuple is assigned to the node that comes clockwise after it
- To delete a node, simply reassign all its tuples to the next node that comes clockwise
- To add a node, split the largest node into 2

>[!note] Multiple markers
>When we remove a node, its tuples will not be fully reassigned to the next node. Instead, it is balanced to different nodes.
---
# Query processing in NoSQL

![mongo-db-architecture|500](Screenshot%202024-04-25%20at%2010.17.36%20PM.png)

---