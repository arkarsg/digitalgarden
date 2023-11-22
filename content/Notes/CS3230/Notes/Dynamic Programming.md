In dynamic programming, we are breaking up a problem into a series of overlapping subproblems and build up solutions to larger and larger subproblems

---

# Weighted interval scheduling
- Label jobs by finishing time: $f_1 \leq f_2 \leq ... \leq f_n$

==Define== $p(j)$ to be the largest index $i < j$ such that $i$ is compatible with $j$

==Define== $OPT(j)$ to be the value of optimal solution to the problem consisting of job requests $1, 2, … , j$

**Case 1** : OPT selects job $j$
- Can’t use incompatible jobs { $p(j) + 1, p(j) + 2, … , j-1$ }
- Must include optimal solution to problem consisting of remaining compatible jobs $1, 2, …, p(j)$

**Case 2** : OPT does not select job $j$
- Must include optimal solution to problem consisting of remaining compatible jobs $1, 2, …, p(j)$

---

This forms the optimal substructure where:
![[optimalsubstructure.png| -m | -center]]


>[!note] Proving optimality
>Must include optimal substructure

Note that the recursive calls for family of layered instances grows. As such, recursive algorithm fails because of redundant sub-problems which produces an exponential algorithm

## Memoization
We store results of each sub-problem in a cache and lookup as needed. Then, before recursing, we check if result exists in the lookup.

With memoization, the run time is $O(n \log n)$ as:
- Sort by finish time : $O(n \log n)$
- Computing will become $O(n)$ after sorting by start time

---

## Finding a solution

```plain-text
Run M-Compute-Opt(n)
Run Find-Solution(n)

Find-Solution(j) {
   if (j = 0)
		output nothing  
	else if (vj + M[p(j)] > M[j-1])
		print j
		Find-Solution(p(j))
	else
		Find-Solution(j-1)
}
```

---

# Bottom-up dynamic programming
This is known as *unwind recursion*

```plain-text

Input: n, s1,...,sn , f1,...,fn , v1,...,vn  
Sort jobs by finish times so that f1 <= f2 <= ... <= fn. Compute p(1), p(2), ..., p(n)

Iterative-Compute-Opt {
   M[0] = 0
   for j = 1 to n
	   M[j] = max(vj + M[p(j)], M[j-1])
}
```

---

# Changing coins

Let `M[j]` be the fewest number of coins needed to change `j` cents
Let the denominations available be $d_1, d_2, … , d_k$

>> Write a recursive formula for `M[j]` in terms of `M[i]` with $i < j$.

==Optimal Substructure==
Suppose $M[j] = t$ meaning that
$$
j = d_{i_1} + d_{i_2} + ... + d_{i_t}
$$

for some $i_1, … , i_t \in \{1,...,k\}$. Then if $j’ = d_{i_1} + d_{i_2} + ... + d_{i_t-1}$, $M[j’] = t - 1$ because otherwise if $M[j’] < t - 1 \implies M[j] < t$.

![[coinchange.png| -s | -center]]

```plain-text
Num_coins_dp(n, d):
	for j = 0, ... , n:
		M[j] = inf
	M[0] = 0
	for j = 1, ... , n:
		for i = 1, ... , k:
			if (j - d_i >= 0) and (M[j - d_i] + 1 < M[j]):
				M[j] = M[j - d_i] + 1
	return M[n]
```

---

# Knapsack problem

Given $n$ objects where
- items weighs $w_i > 0$ and has value $v_i > 0$
- knapsack has a max capacity of $W$

How to fill knapsack so as to maximise total value?

---
>[!caution] Non-solution


==Define== $OPT(i)$ to be the max profit of subset of items $1, … , i$

**Case 1** : OPT does not select item $i$
- OPT selects the best of { $1, 2, …, i-1$ }

**Case 2** : OPT selects item $i$
- Accepting item $i$ does not immediately imply that we will have to reject other items
- Without knowing what other items were selected before $i$, we don’t even know if we have enough room for $i$
---
## Optimal substructure

==Define== $OPT(i, w)$ to be the max profit subset of items $1, … , i$ with weight limit $w$.

**Case 1** : OPT does not select $i$
- OPT selects {$1, … , i-1$ } using weight limit $w$

>[!note] In other words…
>If $i$ is not in the solution, then $OPT(i, w) = OPT(i-1, w)$ since we can simply ignore item $i$

**Case 2** : OPT selects item $i$
- New weight limit = $w - w_i$
- OPT selects the best of {$1, … , i-1$} using the new weight limit
>[!note] In other words
>if $i$ is in the solution, then $OPT(i, w) = w_i + OPT(i-1, w - w_i)$ since we now seek to use the remaining capacity of $w - w_i$ in an optimal way across items $1, 2, …, n - 1$

![[knapsack.png| -m | -center]]

---

## Approach

```plain-text
Input: n, w_1, ... , w_n, v_1, ... , v_n

for w = 0 to W:
	M[0, w] = 0

for i=1 to n:
	for w=1 to W:
		if (w_i > w):
			M[i, w] = M[i-1, w]
		else:
			M[i, w] = max{ M[i-1, w], v_i + M[i-1, w-w_i] }
```

![[knapsacktable.png| -m | -center]]

### Running time

**Running time** is $\Theta(n W)$
- also known as *pseudo-polynomial*

>[!note] Others
>Decision version of Knapsack is NP-complete
>
>**Knapsack approximation algorithm** : there exists a polynomial algorithm that produces a feasible solution that has value within 0.01% of optimum
>[[Approximation Algorithms#Knapsack problem]]

---

# Sequence alignment

Given 2 strings, how similar are the 2 strings?
This is the basis for *Unix diff*

---
## Edit distance
- Gap penalty $\delta$ and mismatch penalty $\alpha_{pq}$
- Cost = sum of gap and mismatch penalties
---

>> Given two strings, $X$ and $Y$, find *alignment* of minimum cost

==Define== *alignment* M as a set of ordered pairs $x_i - y_j$ such that each item occurs in at most one pair and ==no crossings==.

==Define== The pair $x_i - y_j$ and $x_i' - y_j'$ to **cross** if $i < i’$ but $j > j’$

Place one words on top of the other, with gaps in the first word indicating insertions and gaps in the second word indicating deletion.

| F   | o   | o   |     | D   |
| --- | --- | --- | --- | --- |
| M   | o   | n   | e   | y    |

Then, an alignment is a set of $M$ of pairs $(i, j)$ such that each index appears at most once, and there is no crossing. We have the ordering { (1,1), (2,2), (3,3), (4,5) }

→ Cost of an alignment is the number of mismatched columns plus the number of unmatched indices in both strings

---

## Optimal substructure

==Define== $OPT(i, j)$ to be the min cost of aligning strings $x_1, x_2, …, x_i$ and $y_1, y_2, … , y_j$.

**Case 1** : OPT matches $x_i - y_j$
- pay mismatch for $x_i - y_j$ + min cost of aligning 2 strings $x_1, x_2, …, x_{i-1}$ and $y_1, y_2, … , y_{j-1}$

**Case 2a** : OPT leaves $x_i$ unmatched
- Pay gap for $x_i$ and min cost of aligning $x_1, x_2, …, x_i$ and $y_1, y_2, … , y_j$

**Case 2b** : OPT leaves $y_j$ unmatched
- Pay gap for $y_j$ and min cost of aligning $x_1, x_2, …, x_{i-1}$ and $y_1, y_2, … , y_{j-1}$

![[sequencealignment.png| -m | -center]]

```plain-text
Sequence-Alignment(m, n, X, Y, delta, alpha) {
	for i = 0 to m
		M[0, i] = i delta
	for j = 0 to n
		M[j, 0] = j delta

	for i = 1 to m
		for j = 1 to n
			M[i, j] = min(alpha[x_i, y_j] + M[i-1, j-1],
							delta + M[i-1, j],
							delta + M[i, j-1])
	return M[m, n]
}
```

## Running time

- $\Theta(mn)$ time and space

---

# Dijkstra’s algorithm : Proof of correctness

**Invariant** : For each node $u \in S, d(u)$ is the length of the shortest $s-u$ path.

**Base Case** : $| S | = 1$ is trivial
**Inductive hypothesis**: Assume true for $|S| = k \geq 1$
- Let $v$ be the next node added to $S$, and let $u-v$ be the chosen edge
- The shortest $s-u$ path plus $(u, v)$ is an $s-v$ path of length $\pi(v)$
- Consider any $s-v$ path $P$. We will see that it is no shorter than $\pi(v)$
- Let $x-y$ be the first edge in $P$ that leaves $S$, and let $P’$ be the subpath to $x$
- $P$ is already too long as soon as it leaves $S$

Therefore,

$$
l(P) \geq l(P') + l(x, y) \geq d(x) + l(x, y) \geq \pi(y) \geq \pi(v)
$$

---

# Shortest path

Given a *directed graph* $G = (V, E)$ with edge weights $c_{vw}$ with negative weights allowed, find the shortest path from node $s$ to node $t$

Note that `Dijkstra` can fail if there are negative edge costs, and re-weighting by adding a constant to every edge weight can also fail.

#### Observation
1. If some path from `s` to `t` contains a negative cost cycle, there does not exist a shortest path `s-t` path. Otherwise, there exists one that is simple

==Define== $OPT(i, v)$ to be the length of the shortest $v-t$ path $P$ using at most $i$ edges

**Case 1** : $P$ uses at most $i-1$ edges
- $OPT(i, v) = OPT(i-1, v)$

**Case 2** : $P$  uses exactly $i$ edges
- if $(v, w)$ is the first edge, then OPT uses $(v,w)$ and then selects best $w-t$ path using at most $i-1$ edges

![[shortestpath.png| -m | -center]]

By our observation, if no negative cycles, then $OPT(n-1, v)$ is the length of the shortest $v-t$ path

```plain-text
Shortest-Path(G,t) {
	for each node v in V
		M[0, v] = inf
	M[0, t] = 0

	for i = 1 to n-1
		for each node v in V
			M[i, v] = M[i-1, v]
		for each edge (v, w) in E
			M[i, v] = min( M[i, v], M[i-1, w] + c )
}
```

**Memory** : $O(m + n)$
**Running time** : $O(mn)$ worst case

## Bellman-Ford : Efficient implementation

```Push-Based-Shortest-Path(G, s, t) {
	for each node v in V {
		M[v] = inf
		successor[v] = None
	}

	M[t] = 0
	for i = 1 to n - 1 {
		for each node w in V {
			if M[w] has been updated in the previous iteration {
				if M[v] > M[w] + c_vw {
					M[v] = M[w] + c_vw
					successor[v] = w
				}
			}
		}
		If no M[w] value changed in iteration i, stop
	}
}
```

---

# Negative Cycles in a Graph

>[!note] Proof with Bellman-Ford algorithm
>If $OPT(n, v) = OPT(n-1, v)$ for all $v$, then no negative cycles

>> If $OPT(n, v) < OPT(n - 1, v)$ for some node $v$, then any shortest path from $v$ to $t$ contains a cycle $W$. Moreover, $W$ has negative cost.

**Proof by contradiction**
- Since $OPT(n, v) < OPT(n-1, v)$, we know that $P$ has exactly $n$ edges
- By pigeonhole principle, $P$ must contain a directed cycle $W$
- Deleting $W$ yields a $v-t$ path with $< n$ edges $\implies$ W has negative cost.

## Detecting negative cycles
>> Can detect negative cost cycle in $O(mn)$ time

1. Check if $OPT(n, v) = OPT(n-1, v)$ for all nodes $v$
2. If `yes` then no negative cycles
3. If `no` then extract cycle from shortest path from $v$ to $t$

---