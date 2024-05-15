>[!note]
>The following notes refer to `MaxHeap`
>
>In Python `heapq` and Java `PriorityQueue`, the heap is a min-heap

A Binary heap is a *complete* binary tree that maintains the Max Heap property.

>[!note] Complete binary tree
>Every level in the binary tree, except the last/lowest level, is *completely* filled, and all vertices in the last level are as far left as possible.

>[!note] Max Heap property
>The parent of each vertex contains a value greater than the value of that vertex.
>
>In other words, the value of a vertex, except the leaf, must be greater than the value of its children

Based on the Max Heap property, the largest key will be located at the **root**

---

# Priority Queue
Priority queue is similar to normal Queue but
1. `enqueue(x)` — put a new element into the PQ
2. `elem = dequeue()` — Return an existing element that has the highest priority key in the PQ. 

## Properties
### Binary heap has $O(\log N)$ height
For a binary heap of $N$ elements, its height will not be taller than $O(\log N)$

The size of $N$ of a full binary tree of height $h$ is,

$$
N = 2^{h+1}-1
$$

Therefore,
$$
h = \log(N+1)-1
$$

### Compact array
Stored efficiently as a compact array, $A$.

There is no gap between vertices of a complete binary tree.

Using 1-based array simplifies navigation operations

![maxheap|500](https://iq.opengenus.org/content/images/2019/06/Max-Heap.png)

Suppose an array $A = [a_1, ..., a_N]$ and an element of $A$, $a_i$:
1. `parent(a_i) = i >> 1` (index $i$ divided by 2)
2. `left(i) = i << 1` (index $i$ multiplied by 2)
3. `right(i) = (i << 1 ) + 1` (index $i$ multiplied by 2 and add 1)

>[!caution]
>In Python’s implementation of the MaxHeap in `heapq`, it is 0-based

---

# MaxHeap operations
- `create(A)`
	- $O(N \log N)$
	- $N$ calls of `insert`
- `create(A)`
	- $O(N)$
- `insert(v)`
	- $O(\log N)$
- `extractMax()`
	- Once, in $O(\log N)$
	- $K$ times in $O(K \log N)$, also known as `partialSort`
	- $N$ times in $O(N \log N)$, also known as `heapSort`
- `update(i, newValue)`
	- $O(\log N)$ if $i$ is known
- `delete(i)`
	- $O(\log N)$ if $i$ is known


### `insert`

Insertion of a new element into a binary max heap can only be done at the last index $N + 1$ to maintain the compact array.

However, MaxHeap property may be violated as the key may not satisfy the MaxHeap property.

The `insert` operation then satisfies the MaxHeap property by *bubbling the element upwards* until MaxHeap property is not violated.

### `extractMax`

The reporting and then deletion of max element of MaxHeap requires existing element to replace the root.

The element is the **last index** $N$ to maintain the compact array

Promoting the last element of $A$ most likely violates the MaxHeap property

The `extractMax` then satisfies the MaxHeap property by *bubbling the element downwards* until MaxHeap property is satisfied

`extractMax` needs to check **both** children and swap with the *larger* of its two children.
>[!note] Why?
>Otherwise, we may still violate the MaxHeap property.

---

### `create`

There exists 2 versions of `create`

- Calling `insert` $N$ times
	1. Every insertion triggers a path from insertion upwards to the root
	2. This is an $O(N \log N)$ operation

$O(n)$ create by taking advantage of the fact that the first $N/2$ elements are leaf vertices



![o-n-binary-heap|500](Pasted%20image%2020240510223216.png)
Starting from the bottom,

- At $h = 0$, there are ${n}/{2^1}$ *green* nodes
- At $h = 1$, there are ${n}/{2^2}$ *red* nodes
- At $h = 2$, there are $n / 2^3$ *blue* nodes

In general, for height $h$, there are $n / 2^{h+1}$ nodes

Therefore,
- Green nodes : No swap iterations since there are no children
- Red nodes : At most 1 swap operation for each node
- Blue nodes : At most 2 swap operation for each node
- Purple nodes : At most 3 swap operation for each node

Total bubble up operations:
$$
n * ( 0 + ¼ + 2/8 + 3/16 + ... + h/2^{h+1})
$$
For any value of $h$, the total number of operations will never exceed $n \implies O(n)$


