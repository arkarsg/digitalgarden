---
title: Spark
---
# Motivation


# Spark
- Big data processing solution
- Leaves storage to users
- Considered an improvement from Hadoop foundation
---
# Motivation
## Hadoop vs Spark

### Issues with MapReduce
- Network and disk I/O costs
	- intermediate data has to be written to local disks and shuffle across machines, which is slow
	- Not suitable for **iterative** algorithms and processing
	- Each iteration requires 1 read from HDFS and 1 write to HDFS
### Advantages of Spark
 **Spark** stores most of its intermediate results in *memory*, making it much faster, especially for iterative processing
 
 >[!note]
 >When mem is insufficient, Spark spills to disk which requires disk I/O

- Ease of programmability
	- Not a trivial problem for Java Hadoop
- Spark core and Spark SQL engine supports different languages
- Batch processing –> Very efficient with Spark SQL
- Streaming and Graph processing –> Not very efficient
- ML (iterative algorithms) –> Still good

---
# Basics

## Spark architecture

![spark-architecture|500](Screenshot%202024-03-10%20at%2011.37.43%20AM.png)

**Driver process**
- Accepts the requests from user and start a Spark session
- Assigns a job to executor

**Executor**
- Performs jobs in parallel

**Cluster manager**
- How many jobs can be assigned to a machine
- Can be Spark’s standalone cluster manager, YARN, or K8s

**Local mode**
- All the processes run on the same machine

---

## Spark APIs
### Resilient Distributed Datasets (RDDs)
- A collection of JVM objects
- Functional operators (map, filter, etc)

### DataFrame
- A collection of Row objects
- Expression-based operations
	- Much easier than functional operators
- Logical plans and optimiser

### DataSet
- Internally : rows
- Externally : JVM objects

---

# RDDs
- **Resilient** : Achieve fault tolerance through ==lineages==
- **Distributed Datasets**: Represents a collection of objects that is ==distributed over machines==

```python
# Create an RDD of names, distributed over 3 partitions
dataRDD = sc.parallelize(['Alice', 'Bob', 'Carol', 'Daniel'], 3)

# Create an RDD: length of names -- transformation
nameLen = dataRDD.map(lambda s: len(s))
```
- ==Immutable== : Cannot be changed once created
- Therefore, we need ==transformations==

### Transformations
Transformations are a way of transforming RDDs into RDDs.
- Examples of transformations:
	- `map`
	- `order`
	- `groupBy`
	- `filter`
	- `join`
	- `select`

In Spark, transformations are *lazy*. Not executed until an ==action== is called on it.

```python
# Create an RDD of names, distributed over 3 partitions
dataRDD = sc.parallelize(['Alice', 'Bob', 'Carol', 'Daniel'], 3)

# Create an RDD: length of names -- transformation
nameLen = dataRDD.map(lambda s: len(s))

# Action - Retrieve all elements of the RDD to the driver node
nameLen.collect()
```

>[!note]
>If there is no *action*, Spark will just create a ==lineage==

>[!note] Why lazy transformation?
>Spark is a big data system. Therefore, it needs to execute in the most efficient way. If there are many transformations, Spark will optimise by reordering for example, to improve its efficiency.


## Working with RDDs
![rdd|500](Screenshot%202024-03-10%20at%2011.54.21%20AM.png)
*Starting point* must be from a persistent storage (HDFS, DB, etc)

- Each line creates a lineage that is not executed until an action is called.

---

# Caching

>[!example]
>Load error messages from a log into memory, then interactively search for various patterns
>

```python
lines = sc.textFile("hdfs://...")
errors = lines.filter(lambda s: s.startswith("ERROR"))
messages = errors.map(lambda s: s.split("\t")[2])
messages.cache()

messages.filter(lambda s: "mysql" in s).count() # action
messages.filter(lambda s: "php" in s).count() # 2nd action
```

1. Driver node sends tasks to workers
2. Each worker
	1. Read the file
	2. Perform transformations
	3. Cache data
	4. Calculate count and send to driver

With `cache`, the worker can directly use the file from cache and send back to the driver node.
Without `cache`, the 2nd action will start from the driver node

>[!note]
>Reading from memory is faster than reading from disk

#### `cache`
- Saves an RDD to memory *of each worker node*

#### `persist`
- Can be used to save an RDD to memory, disk or off-heap memory

### When to cache?
- When it is expensive to compute and needs to be re-used multiple times
- If worker nodes do not have enough memory, they will evict the ==LRU== RDDs.

---

# Directed Acyclic Graph
- Internally, Spark creates a graph which represents all the RDD objects and how they will be transformed
- *Transformations* constructs this graph
- *Actions* trigger computations on it

This lineage transformation with DAGs is how Spark achieves fault tolerance.
![dag|300](Screenshot%202024-03-10%20at%2012.09.22%20PM.png)
```scala
val file = sc.textFile("hdfs://...")
val counts = file.flatMap(line => line.split(" "))
				.map(word => (word, 1))
				.reduceByKey(_ + _)
counts.save("...")
```

---
## Dependencies

### Narrow dependencies
- Each partition of the parent RDD is used by at **most** one partition of the child RDD. Does not need information from other partition.
	- `map`, `flatMap`, `filter`, `contains` 
	- For example, from the error log example:
		- Parent RDD: `lines`
		- Child RDD: `erorrs`

### Wide dependencies
- Each partition of parent RDD is used by multiple partitions of the child RDD
	- `reduceByKey`, `groupBy`, `orderBy`
- If 1 parent partition communicates with more than 1  child partition
- Requires shuffling
- Need to get info from other worker machines

---
## Stages
Consecutive ==narrow== dependencies are grouped together as *stages*.

### Within stages
Spark performs consecutive transformations on the **same** machines

### Across stages
Data needs to be **shuffled**, exchange across partitions
- Involves writing intermediate results to disk

>[!note]
>Minimising shuffling is good practice for improving performance

---
### Example

```python
df1 = spark.range(2, 1000000, 2) # transformation -- narrow
df2 = spark.range(2, 1000000, 4) # transformation -- narrow

df3 = df1.join(df2, ["id"])      # transformation -- wide

df3.count()                      # action
```
- If the output is an RDD, it is a *transformation*
- `join` is a wide transformation
	- Need to look through all rows with a particular id
	- Need to match and shuffle across the table

---

# Lineage and fault tolerance

- Spark does not use replication to allow fault tolerance
- Spark tries to store all data in memory, not disk.

**Lineage approach** : if a worker node goes down, we replace it by a new worker node, and use DAG to recompute the data in the lost partition
- Only need to recompute RDDs from the lost partition

---
# DataFrames

- A DataFrame represents a table of data, similar to tables in SQL or DataFrames in `pandas`
- Tells Spark what to do, instead of *how* to do it
- Code is far more expressive as well as simpler
- Spark can inspect or parse this query to understand the user’s intention. It can then optimise or arrange the operations to make it more efficient

Compared to RDDs, this is a higher level interface. Transformations resemble SQL operations.

>[!caution] 
>All DataFrame operations are still ultimately compiled down to RDD operations by Spark

---

# Spark SQL

- Spark can connect to a lot of storage solutions (incl HDFS, SQL, NoSQL, Kafka)
- SQL does not imply SQL language. It just means relational operation.
- This is because most business data are in tabular format

## Catalyst optimiser
Takes a computational query and converts it into an execution plan through 4 transformational phases:
1. Analysis
2. Logical computation
3. Physical planning
4. Code generation

## Tungsten
- Substantially improve the memory and CPU efficiency of Spark applications
- Push performance closer to the limits of modern hardware

