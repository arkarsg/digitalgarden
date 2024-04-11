Given a big data system program, 
- Analyzing scalability
- Analyzing disk I/O and network I/O performance
- Analyzing memory consumption
	- Need to care about memory consumption as out of memory is very common
- Analyzing load balance

# Performance guidelines
- Linear scalability
	- More nodes can do more work in the same time
	- Linear on data size
	- Linear on compute resources
- Minimise the amount of I/Os in hard disk and network
	- Minimise disk I/O; sequential vs random
	- Minimise network I/O; bulk send/ receive vs many small send/ receive
- Memory working set of each task/worker
	- Large memory working set → high memory requirements / probability of out-of-memory errors

---

## Step-by-step performance analysis

### Scalability analysis
- **Max number of map tasks** : Will the number of *mapper tasks* increase linearly as the input size increases?
- **Max number of reduce tasks** : Will the number of *reducer tasks* increase linearly as the input size increases?

### I/O analysis
- input + intermediate results + output
- The amount of ==disk== I/O from each Map/Reduce task
- the amount of ==network== I/O from each Map/Reduce task
- the amount of ==network== I/O in shuffle (intermediate results from map tasks)

### Memory working set
- *Intermediate results* in the main memory
- The amount of memory consumption from each map/reduce task

---

# Example

## Version 0

```python
class Mapper:
	def map(key: Long, value: Text):
		for (word in tokenize(value)):
			emit(word, 1)

class Reducer:
	def reduce(key: Text, values: Iterable[int]):
		for value in values:
			sum += value
		emit(key, sum)
```

### Scalability analysis
Suppose 1 worker can run 1 `map` or `reduce` task.

>> Given $W$ workers, we can run $W$ tasks at the same time

Given the input, what is the;
- Max number of map tasks $\implies \lceil \text{input size} / \text{chunk size} \rceil$
- Max number of reduce tasks $\implies$ number of distinct keys
	- Suppose there is only $1$ distinct word. Then, `values` will be in the scale of the large data

>[!note] Why are we interested in `max`?
>The number of workers needed is limited by the number of tasks

---
### I/O Analysis
For a MapReduce job,
- Reading input from HDFS — *mainly* disk I/O
- Shuffle and sort — disk and network I/O
- Output — disk and network I/O

#### Map task
- Input disk I/O → one chunk → $128MB$
- Output disk I/O → All `<word, 1>` pairs → number of words in the chunk
- Network I/O → very small as it is executed on the local machine (unless there are failures)

#### Shuffling
- Network I/O → All `word, 1` pairs → number of words in the chunk ==(assuming combiner is not used)==

#### Reduce task
- Input disk I/O → very small (input data is from the network)
	- *Already counted in shuffling* – `reduce` task will read remotely from output of the `map` task
- Intermediate results → very small
- Output disk I/O → very small
- Network I/O → very small
`key, sum` is output to HDFS

### Memory consumption
#### Map task
- Memory working set → depends on `tokenize` → small if `tokenize` is memory efficient

#### Reduce task
- Reading `key, values` from other machines
- The only variable maintained in the main memory is the `sum` → small memory working set
---

## Version 1

```python
class Mapper:
	def map(key: Long, value: Text):
		val counts = new Map()
		for word in tokenize(values):
			counts[word] += 1
		for key, value in counts:
			emit(key, value)
```

In comparison the `Version 0`, the mapper uses a hash table to maintain the words and counts *per document*. After processing each document, it emits the counts for the line.

>[!example]
>Suppose a document consists of `1` word $n$ number of times.
>- *Version 0* will emit $n$ times
>- *Version 1* will only emit **once**
>
>Works better when there are duplicate words

### Scalability

### I/O analysis
#### Map task
- Input disk I/O : $128MB$
- Intermediate results : *very small*
	- need to understand the size of the hashtable
	- Hashtable contains thousands of words and thousands of counts $<<$ main memory
	- Worst case: Overflow the main memory when there are a lot of distinct words
- Output disk I/O : all `word, count` pairs → Number of distinct words in each document
- Network I/O : very small
- Memory working set : hash table size

#### Shuffling
- Network I/O : All `word, count` pairs → Number of distinct words in each document

---
## Version 2

```python
class Mapper:
	val counts = new Map()

	def map(key: Long, value: Text):
		for word in tokenize(value):
			counts[word] += 1

	def cleanup():
		for key, value in counts:
			emit(key, value)
```

Instead of removing duplicates one document per chunk at a time, the `map` is now class-level. `map` handles duplicates *across* documents in a chunk.

>[!note] Preserve state across input key-value pairs

- Memory consumption of `map` : ~ $100MB$ → Has a minimum requirement

Therefore this is efficient in terms of I/O but may cause a lot of OOM.

