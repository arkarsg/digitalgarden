
>[!note] Key idea
>Linked list is a data structure consisting of a group of *nodes* which together represent a *sequence*


# List

List is a sequence of nodes where positional order matter

Common operations
- `get(i)` — return $a_i$
- `search(v)` — decide if node $v$ exists and return its index
- `insert(i, v)` — insert node $v$ specifically at index $i$, potentially shifting items from previous positions
- `remove(i)` — remove item that is at position $i$

## Array

Array implements the list ADT. Let array $A$ be a compact array

>[!note] Compact array
>For an array of size $M$ with $N$ items, only the index $[0, ..., N-1]$ are occupied and $[N, …, M]$ remains empty. Between the items, there are no **gaps**

The size of $M$ is a finite number.
- Too small –> run out of space easily
- Too big –> unused space wasted

Python `List`, Java’s `Vector` and `ArrayList` are variable-sized arrays. When an array is full, a larger array of 2 * $M$ is created and move elements from old $A$ to new $A$. This still incurs an overhead.

### Array implementation
- `get`
	- Return $A[i]$
	- Array indexing –> $O(1)$
- `search`
	- In the worst case, $v$ does not exist
	- Requires $O(N)$ scan of $A$
- `insert`
	- Inserting at the tail of the array –> $O(1)$
	- Inserting at the start of the array –> $O(N)$ as it requires $N$ elements to shift
- `remove`
	- Removing at the tail of the array –> $O(1)$
	- Removing at the start of the array –> $O(N)$
---
## Linked list
Linked list data structure uses *pointers* to allow nodes to be **non-contiguous** in memory. Suppose for $A = \{ a_0, …, a_n\}$, $a_i$ and $a_{i+1}$ are associated through a pointer.

The linked list node has 2 fields
- `value` of type `int`
- `next` of type pointer to `Node` 

We only keep head and tail pointers.

```cpp
struct Vertex {
	int value;
	Vertex* next;
}
```

```python
class Vertex {
	def __init__(self, value):
		self.value = value
		self.next = None
}
```

```go
type Node struct {
	value int
	next *Node
}
```

### Linked list implementation
- `get`
	- Slower than array
	- List traversal subroutine is needed to reach positions other than index $0$ and index $N-1$
	- $O(N)$

```go
func get(i int) *Node {
	if i < 0 || head == nil {
		return nil
	}

	pointer := head;
	for k := 0; k < i; k++ {
		ptr = ptr.next
	}
	return pointer
}
```

- `search`
	- Start from head node and traverse through the pointers
	- $O(N)$
- `insert`
	1. Insert at head — $O(1)$
		- Point $v_{new.next}$ to $head$
		- Point $head$ to $v_{new}$
		- Handle insertion into empty list
	2. Insert in between linked list — $O(N)$
		- `get` to $i-1$-th node — $prev$ node
		- $aft$ –>$prev_{next}$
		- $v_{next} = aft$
		- $prev_{next} = v$
	3. Beyond the tail $i = N$ — $O(1)$
		- Point $tail_{next}$ to $v$
		- Update the tail pointer $tail = v$
- `remove`
	1. Remove at head — $O(1)$
		- Assign $v$ as $head$
		- Point $head$ to $head_{next}$
		- Delete $v$
	2. Remove between linked list — $O(N)$
		- Assign $prev$ as `get(i - 1)`
		- Assign $v$ as $prev_{next}$
		- Assign $aft$ as $v_{next}$
		- Delete $v$
	3. Remove at tail — $O(N)$
		- Assign $pre$ as $head$
		- Assign $tmp$ as $head_{next}$
		- While $tmp$ is not the tail:
			- $pre = pre_{next}$
			- $tmp = tmp_{next}$
		- Assign $pre_{next}$ as `null`
		- Delete $tmp$
		- Assign $tail$ as $pre$
---

# Stack
Stack is an ADT whose main operation is addition of an item to the collection known as `push` to the top of the stack and removal of item, known as `pop` from the top of the stack.

It is a Last-In-First-Out data structure.

In other words, Stack is a **protected** Linked list where we can only peek, insert and remove from the head. These operations are all $O(1)$

>[!example] Some problems
>1. Bracket matching
>2. Postfix expression calculator

---

# Queue
Queue is an ADT whose items in collections are kept in order and the main operations on the collection are addition of items to the back and removal from the front

It is a First-In-First-Out data structure

>[!caution] Why array is not the most suitable implementation
>Insertion at the back is $O(1)$, but removal at the front is $O(N)$
>
>To avoid shifting, maintain 2 indices `front` and `back` which are updated with `enqueue` and `dequeue` operation.
>
>However, when the array reaches its size limit, you cannot queue even if the indices before `front` is empty.
>To solve this, allow both `front` and `back` to wrap back to index $0$
>
>An alternative is to implement a queue using 2 stacks

Since we do not know the upper bound of the queue size, Linked list are used to implement a queue

---

# Doubly linked list
Similar to Singly linked list, but each node contains 2 pointers. For some node $a_i$,
- `next` points to $a_{i+1}$ if the node exists
- `prev` points to $a_{i-1}$ if the node exists

`prev` pointers allow backward iteration of linked list. This improves the following specs from Singly Linked List

1. Remove at tail — $O(1)$
	1. Assign `tmp` as `tail`
	2. Assign `tail` as `tail.prev`
	3. Assign `tail.next` as `null`
	4. Delete `tmp`


