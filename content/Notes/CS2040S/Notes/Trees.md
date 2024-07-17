>[!note]
>Connected *acyclic* graphs where 2 vertices are connected by only 1 path with $|V| - 1$ edges in total

## Binary search trees
>[!note]
>A tree which is either *empty* or has *left* and *right* children binary trees

- A binary search tree property states that all keys in left sub tree are less than the parent key and all keys in the right sub tree are greater than the parent key
- The *height* of a BST is the number of edges on the longest path from the root to the leaf

The height of a binary tree, with root node $v$, $h(v)$ has the recursive substructure:
1. $0$ if $v$ is a leaf
2. $-1$ if $v$ is null
3. $\max \Big(h(v.left), h(v.right)\Big) + 1$

#### Searching
Searching for a specify key is done by comparing the key with the parent key, recursively searching $v.left$ if less than and $v.right$ if greater than, and stopping if equal
#### Inserting
Add new node at a leaf, that fulfils the BST property
#### Deleting
- Trivial if node has one or no children
- Else, the node to be deleted has to be replaced by the minimum of the right subtree

To delete a node in such a way that the resulting tree follows BST, find the inorder successor of the node.

1. If the right subtree of $v$ is not `null`, then the successor lies in the right subtree
2. If the right subtree of $v$ is `null`, then successor is one of the ancestors → travel up the tree until you see a node which is left child of its parent. The parent of such a node is the successor

```
successor(v)
	if v has right child:
		return the min key in v.right
	else:
		walk up the tree to a node w where w.parent.left == w or w is the root
		return w
```

---

## AVL Trees
>[!note]
>AVL trees are augmented BST which stores the tree height in each node

This augmented height field must be updated with every `insert` and `delete` operation.

- A binary search tree is **balanced** $\iff$ $h = O(\log n)$ and all operations take $O(\log n)$ time
- A node $v$ is **balanced** $\iff$$| v.left.height - v.right.height | \leq 1$




