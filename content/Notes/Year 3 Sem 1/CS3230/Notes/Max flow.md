# Minimum cut problem
## Flow network
- An abstraction for material flowing through the edges
- $G = (V, E)$ which is a *directed* graph with no parallel edges
- Define $s$ as the source node and $t$ as the sink node
- $c(e)$ is the capacity of edge $e$

![[Screenshot 2023-10-16 at 11.51.47 PM.png|80%]]

>[!note] Cut
>Define an $s-t$ cut as a partition $(A, B)$ of $V$ with $s \in A$ and $t \in B$

The ==capacity== of the cut is the sum of the capacities of outgoing edges from the partition.

>[!aside | right +++++]
>Note that the edges into $A$ are not considered in the capacity of the cut

![[Screenshot 2023-10-16 at 11.54.15 PM.png|80%]]

---

## Flows
### Problems
- [i] Find an $s-t$ cut of minimum capacity
- [i] Find an $s-t$ cut of minimum capacity

---
#### $s-t$ flow
An $s-t$ flow is a function that satisfies:
1. For each $e \in E, \space 0 \leq f(e) \leq c(e)$
	- In other words, the *flow* in an edge cannot exceed the capacity of the edge
2. For each $v \in V - \{s, t \} \space \sum_{\text{e into v}} f(e) = \sum_{\text{e out of v}} f(e)$
	- In other words, the flow is *conserved* (whatever comes in must go out)

The *value* of a flow is $v(f)  = \sum_{\text{e out of s}} f(e)$

---

#### Flow value lemma
Let $f$ be any flow, and let $(A, B)$ be any $s-t$ cut. Then, the net flow sent across the cut is equal to the amount leaving $s$
$$
\sum_{\text{e out of A}} f(e) - \sum_{\text{e in to A}} f(e) = v(f)
$$

In this case, if there exists a flow that is entering $A$, then we need to deduct the flow value from it.

![[Screenshot 2023-10-17 at 12.08.26 AM.png|80%]]

**Proof**
1. Value of flow : $v(f)  = \sum_{\text{e out of s}} f(e)$
2. By flow conservation, all terms except $v = s$ are 0
3. 
$$
\sum_{v \in A} \Big(
\sum_{\text{e out of v}} f(e) - \sum_{\text{e in to v}} f(e) \Big)
$$

---

#### Weak Duality

Let $f$ be any flow, and let $(A, B)$ be any $s-t$ cut. Then the value of the flow is at most the capacity of the cut

![[Screenshot 2023-10-17 at 12.17.14 AM.png|80%]]

![[Screenshot 2023-10-17 at 12.17.38 AM.png|80%]]

---

#### Optimality
Let $f$ be any flow, and let $(A, B)$ be any cut. If $v(f) = cap(A, B)$, then $f$ is a max flow and $(A, B)$ is a min cut

---

## Max flow algorithm
>[!note] Greedy may not work
> Consider the greedy algorithm
> ```
> Start with f(e) = 0 for all edge e in E
> Find an s-t path P where each edge has f(e) < c(e)
> Augment flow along path P
> Repeat until you get stuck
> ```
> 
> The greedy algorithm may not work as it finds the local optimum $\neq$ global optimum

![[Screenshot 2023-10-17 at 12.23.51 AM.png|80%]]

### Residual graph

For an *original edge* $e = (u, v) \in E$, let flow = $f(e)$ and capacity = $c(e)$, the residual edge is the *opposite* of the flow edge : $e^R = (v, u)$

![[Screenshot 2023-10-17 at 12.27.02 AM.png|80%]]

Then, we can construct a *residual graph* from residual edges with *positive* residual capacity

```
Augment(f, c, P) {
	b = bottleneck(P)
	for each e in P {
		if e in E
			f(e) = f(e) + b
		else
			f(e_r) = f(e) - b
	}
	return f
}
```

```
Ford-Fulkerson(G, s, t, c) {
	for each e in E, f(e) = 0
	G_f = residual graph

	while there exists augmenting path P {
		f = Augment(f, c, P)
		update G_f
	}
	return f
}
```

In the algorithm, we repeatedly find the *augmented paths* through the *residual graph* .

The augmenting path will have a *bottleneck* value, which is the smallest edge on the path. Then, we use the bottleneck value to *augment the flow* along the path.

==Augmenting the flow== refers to updating the flow values of the edges along the augmenting path. For *forward edges*, this means increasing the flow by bottleneck value.

Residual edges exist to “undo” bad augmenting paths which do not lead to a maximum flow.

>[!tip]
>The sum of the bottlenecks found in each augmenting path is equal to the max-flow
---

### Proof
>[!note] Augmenting path theorem
>Flow $f$ is a max flow iff there are no augmenting paths

>[!note] Max-flow min-cut theorem
>The value of the max flow is equal to the value of the min cut

1. There exists a cut $(A, B)$ such that $v(f) = cap(A, B)$
2. Flow $f$ is a max flow
3. There is no augmenting path relative to $f$

- $1 \implies 2$ due to [[Max flow#Weak Duality]]
- $2 \implies 3$ can be show by contrapositive
	- Let $f$ be a flow. If there exists an augmenting path, then we can improve $f$ by sending flow along path.
- $3 \implies 1$
	- Let $f$ be a flow with no augmenting paths.
	- Let $A$ be set of vertices reachable from $s$ in residual graph
	- By definition of $A$, $s \in A$
	- By definition of $f$, $t \notin A$

---

# Choosing good augmenting paths

### Approach
- Choose augmenting paths with
	- Max bottleneck capacity
	- Sufficiently large bottleneck capacity
	- Fewest number of edges

---

## Capacity Scaling

>[!note]
>Choosing path with highest bottleneck capacity increases flow by max possible amount.
>- Maintain scaling parameter $\Delta$
>- Let $G_f(\Delta)$ be the subgraph of the *residual graph* consisting only arcs with capacity at least $\Delta$

```
Scaling-Max-Flow(G, s, t, c) {
	for each e in E, f(e) = 0
	delta = smallest power of 2 greater than or equal to c
	G_f = residual graph

	while (delta >= 1) {
		G_f(delta) = delta-residual graph
		while there exists augmenting path P in G_f(delta) {
			f = augment(f, c, P)
			update G_f(delta)
		}
		delta = delta / 2
	}
	return f
}
```

### Correctness

**Assumption** : All edge capacities are integers between 1 and $C$
**Integrality invariant** : All flow and residual capacity values are integral
**Correctness** : If the algorithm terminates, then $f$ is a max flow
