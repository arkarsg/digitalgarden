# Similarity metric
## Jaccard similarity
$$
S_{\text{Jaccard}}(A, B) = \frac{|A \cap B|}{|A \cup B|}
$$

## Jaccard distance
$$
d_{\text{Jaccard}}(A, B) = 1 - S_{\text{Jaccard}}(A, B)
$$

---
# Similar documents
## Goals
- **All pairs similarity** : Given a large number of $N$ documents, find all *near duplicate* pairs (ie Jaccard distance below a certain threshold)
- **Similarity search** : Given a query document $D$, find all documents which are *near duplicates* with $D$

## Applications
- Mirror websites or approximate mirrors
- Similar news articles — cluster articles by *same story*

---
## Essential steps
1. **Shingling** : Convert documents to sets of short phrases
	- >[!note] Why not just words?
	> A set of words assume that there is no order and loses a lot of meaning.
	- User defines the length of phrase
		- Longer document → longer shingles
		- Shorter document → shorter shingles
2. **Min-Hashing** : Convert these sets to short *signatures* of each document, while preserving similarity
	- Signature is a short piece of information that represents the set
	- Block of data representing the contents in a compressed way
	- Documents with the same signature are candidate pairs

![shingle-hash|500](Screenshot%202024-02-24%20at%2010.16.22%20PM.png)

---
# Shingles
*k-gram* for a document is a sequence of $k$ tokens that appears in the document

Each document $D_1$ can be thought of as a set of its $k-shingles$.

- Often represented as a matrix where columns represent documents and shingles represent rows
- We measure similarity between documents with ==Jaccard similarity== (pairwise)

>[!caution] Similarity metric with shingles 
>Since the comparison is pairwise, the number of similarities comparison is $N(N-1) / 2$ comparisons. For large vocabulary size (number of rows), it will be too slow.

---
# MinHash
- Fast approximation to the result of using Jaccard similarities to compare all documents

==Key idea== : hash each column to a small signature $h(C)$ such that:
1. $h(C)$ is small enough that the signature fits in RAM
2. highly similar documents usually have the same signature

==Goal== : Find a hash function such that:
- If $sim(C_1, C_2)$ is high, then with high probability, $h(C_1) = h(C_2)$
- If $sim(C_1, C_2)$ is low, then with high probability, $h(C_1) \neq h(C_2)$

>[!example]
>1. Given a set of shingles ==(the cat), (cat is), (is glad)==
>2. Hash function $h$ maps each shingle to an integer
>3. Compute the min of these $\min(h_1, h_2, h_3)$

>[!note]
>The probability that two documents have the same MinHash signature is equal to their Jaccard similarity

---
## Extension
- Use $N$ hash functions to generate $N$ signatures for each document.
- Candidate pairs can be defined as those matching a sufficient number among these signatures

>[!caution]
>Hash functions must be *statistically independent*

---
# MapReduce implementation
## Map
- Read over the document, and extract its shingles
- Hash each shingle and take the min of them to get the ==MinHash==
- Emit `<signature, document_id>`

>[!note] 
>In the shuffle step, it will be sorted according to the signature

## Reduce
- Receive all documents with a given ==MinHash== signature
- Generate all candidate pairs from these documents

---
## Performance analysis
### Scalability
- Number of *map* tasks = number of chunks
- Number of *reduce* tasks = number of *distinct* signature

### I/O
- Number of *map* tasks = number of chunks
- Number of *reduce* tasks

---
# Clustering
- Clustering separates unlabelled data into groups of similar points
- Clusters should have high intra-cluster similarity, and low inter-cluster similarity

## K-means
1. Pick $K$ random points as centers
2. Repeat:
	- **Assignment** : Assign each point to nearest cluster
	- **Update** : Move each cluster center to average of its assigned points
	- **Stop** : if no assignments change

## MapReduce implementation
- 1 job → 1 iteration

```python
class Mapper:
	def configure():
		c = load_clusters()

	def map(i: Id, p: Point):
		n = nearest_cluster_id(c, p)
		emit(n: cluster_id, p)

class Reducer:
	def reduce(n: cluster_id, points: Iterable[Point]):
		s = init_point_sum()
		for p in points:
			s = s + p
		m = compute_centroid(s)
		emit(n, m)
```

Output of `reduce` becomes the input for `Mapper`

Disk I/O exchanged between mappers and reducers
- Emitted for each points → $n$ points
- Each point has $d$ dimensions
- There are $m$ iterations

$\implies$ Disk I/O = $O(nmd)$

