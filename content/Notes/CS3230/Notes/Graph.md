
#notes #cs3230 

# Graph representation

## Adjacency matrix

$n * n$ with $A_{uv} = 1$ if $(u. \space v)$ is an edge.

- Space is proportional to $n^2$
- Checking if $(u, \space v)$ is an edge takes $\Theta(1)$ time
- Identifying all edges takes $\Theta(n^2)$ time

## Adjacency list
Node indexed array of lists

- Each edge has 2 representations
- Space is proportional to $m \space + \space n$
- Checking if $(u,v)$ is an edge takes $O(deg(u))$ time, where *degree = number of neighbours of $u$*
- Identifying all edges takes $\Theta(m + n)$ time

---

# Basics

>[!note] Path
>A ==path== in an undirected graph $G = (V, E)$ is a sequence of $P$ of nodes, $v_1, v_2, …, v_{k-1}, v_k$ with the property that each consecutive pair is joined by and edge in $E$.


>[!note] Simple path
>A path is simple if all nodes are distinct.

>[!note] Connected graph
>An *undirected graph* is ==connected== if for every pair of nodes $u$ and $v$, there is a path between $u$ and $v$.

>[!note] Cycles
>A ==cycle== is a path $v_1, v_2, …, v_{k-1}, v_k$ in which $v_1 = v_k, k \gt 2$ and the first $k - 1$ nodes are all distinct.

>[!note] Trees
>An undirected graph is a ==tree== if it is connected and does not contain a cycle.
>
>Therefore, for an undirected graph $G$ on $n$ nodes, if $G$ is connected and $G$ does not contain a cycle → $G$ has $n-1$ edges.

>[!note] Rooted trees
>Given a tree $t$, choose a root node $r$ and orient each edge away from $r$.

---

# Traversal

## Breadth-first search
>[!tip] Intuition
>Explore outward from `s` in all possible directions, adding nodes one *layer* at a time.

>[!note] Theorem
>For each $i$, $L_i$ consists of all nodes at distance exactly $i$ from $s$. 
>There is a path from $s$ to $t$ iff $t$ appears in some layer.

### Properties

>> Let $T$ be a BFS tree of $G = (V, E)$ and let $(x, y)$ be and edge of G. Then, the level $x$ and $y$ differs by at most 1.

---

>> The implementation of BFS runs in $O(m + n)$ time if the graph is given by its adjacency representation.

#### Proof
When we consider a node $u$, there are $deg(u)$ incident edges $(u, v)$. The total time processing edges is $\sum_{u \in v} deg(u) = 2m$.

---

>> BFS gives a connected component R containing $s$.

>[!tip]
>BFS explore in order of distance from $s$.

---

# Bipartiteness

>[!note] Definition
>An undirected graph $G = (V, E)$ is bipartite if the nodes can be colored red or blue such that *every edge* has one red and one blue.

----

>> If a graph $G$ is bipartite, it cannot contain an odd length cycle.


![[2colourable.png|80%]]

---

>> Let $G$ be a connected graph, and let $L_0, …, L_{k}$ be the layers produced by BFS starting at node $s$. Then, *one* of the following holds:
>> > 1. No edge of $G$ joins 2 nodes of the same layer, and $G$ is bipartite.
>> > 2. An edge of $G$ joins 2 nodes of the same layer, and G contains an odd length cycle (not bipartite)

#### Proof

##### 1.
1. Suppose no edge joins 2 nodes in the same layer.
2. By [[Graph#Properties | properties]] of BFS tree, this implies that all edges join nodes on adjacent levels.
3. Then, red = odd levels, blue = even levels.

##### 2.
1. Suppose $(x, y)$ is an edge with $x$ and $y$ in same level $L_{j}$.
2. Let $z$ = lowest_common_ancestor$(x, y)$
3. Let $L_{i}$ be level containing $z$.
4. Consider cycle that takes edges from $x → y → z → x$.
5. Its length is odd.

![[lca.png|30%]]

---

>[!caution] Bipartiteness
>A graph $G$ is bipartite $\iff$ it contains no odd-length cycle.

---

# Directed Graphs

Given $G = (V, E)$, Edge$(u, v)$ goes from node $u$ to $v$.

## Strong connectivity

>[!note] Definition
>Node $u$ and $v$ are *mutually reachable* if there is a path from $u$ to $v$ and also a path from $v$ to $u$.

>[!note] Definition
>A graph is *strongly connected* if every pair of nodes is mutually reachable.

>> Let $s$ be any node. $G$ is strongly connected $\iff$ every node is reachable from $s$ and $s$ is reachable from every node.

---

#### Determine if $G$ is strongly connected in O(m + n) time

1. Pick any node $s$
2. Run BFS from $s$ in $G$
3. Run BFS from $s$ in $G^{rev}$
4. Return true $\iff$ all nodes reached in both BFS executions

---

# DAGs and topological ordering

>[!note] DAGs
>A DAG is a directed graph that contains no *directed cycles*.

>[!note] Topological ordering 
>A *topological order* of a directed graph, $G = (V, E)$ is an ordering of its nodes as $v_1, v_2, … , v_n$ so that for every edge $(v_i, v_j)$, we have $i < j$

This results in the existence of ==precedence constraint== where Edge$(v_i, v_j)$ means task $v_i$ must occur before $v_j$.

---

#### If G has a topological order, then G is a DAG.

1. Suppose that G has a topological order and that G also has a directed cycle C.
2. Let $v_{i}$ be the lowest-indexed node in C and let $v_j$ be the node just before $v_i$, thus $(v_j, v_i)$ is an edge.
3. By our choice of $i$, we have $i < j$.
4. On the other hand, $(v_j, v_i)$ is an edge and there exists a topological order, so we must have $j < i$, a contradiction.

---

#### If G is a DAG, then G has a node with no incoming edges.

1. Suppose that G is a DAG and every node has at least one incoming edge.
2. Pick any node $v$ and begin following the edges backward from $v$. Since $v$ has at least one incoming edge $(u, v)$, we can walk backward to $u$.
3. Then, since $u$ has at least one incoming edge $(x, u)$, we can walk backward to $x$.
4. Repeat until we visit a node $w$ twice.
5. Let $C$ denote the sequence of nodes encountered between successive visits to $w$. $C$ is a cycle.

---

#### If G is a DAG, then G has topological ordering.

1. Base case : true if $n = 1$
2. Given DAG on $n > 1$ nodes, find a node $v$ with no incoming edges.
3. $G - {v}$ is a DAG since deleting $v$ cannot create cycles.
4. By inductive hypothesis, $G- {v}$ has a topological ordering.
5. Place $v$ first in topological ordering, then append nodes of $G - {v}$ in topological order. This is valid since $v$ has no incoming edges.

---

#### There exists an O(m + n) solution to find a topological order.
1. Maintain the following information:
	1. `count[w]` : remaining number of incoming edges
	2. `S` : set of remaining nodes with no incoming edges
2. Initialisation: O(m + n) scan through graph
3. Update:
	1. remove `v` from `S`
	2. decrement `count[w]` for all edges from `v` to `w`, and add `w` to `S` if `count[w]` hits 0

---

