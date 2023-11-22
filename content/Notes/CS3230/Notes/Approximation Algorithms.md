>[!note] 
>Suppose I need to solve an NP-hard problem, then we need to sacrifice one of three desired features
>
>- Solve problem to optimality
>- Most approximation algorithms are greedy


$\rho$-approximation algorithm
- Guaranteed to run in poly-time
- Guaranteed to solve arbitrary instance of the problem
- Guaranteed to find solution within ratio $\rho$ of the true optimum

---

# Load balancing

**Input** : $m$ identical machines; $n$ jobs, job $j$ has processing time $t_j$
- Job $j$ must run contiguously on one machine
- A machine can process at most one job at a time

Let $J(i)$ be the subset of jobs assigned to machine $i$. The *load* of machine $i$ is $L_i = \sum_{j \in J(i) } t_j$

>[!info] Makespan
>The *makespan* is the maximum load on any machine $L = max_i L_i$

Assign each job to a machine to minimise makespan – assign such that maximum load that any machine gets is minimised

>[!example] List-Scheduling algorithm
>Consider $n$ jobs in some fixed order
>Assign job $j$ to machine whose load is smallest so far
>
>```
>List-Scheduling(m, n, t_1, t_2, … ,  t_n)
>	for i = 1 to m
>		L_i = 0 // load on machine i is 0
>		J(i) = None // No jobs assigned to machine i
>	
>	for j = 1 to n
>		i = argmin L_k // select the machine with smallest load
>		J(i) = J(i) + { j } // assign job j to machine i
>		L_i  += t_j         // update load of machine i
>```
>
>**Implementation** : Runs in $O(n \log n)$ using a priority queue

---

## Analysis
Note that the greedy algorithm does not return the optimum solution.

Greedy algorithm is a 2-approximation algorithm (differs by factor 2).

Let $T$ denote the makespan from our algorithm and $T^*$ the minimum optimal makespan. Then, we define a lower bound on the optimum — no matter how good the optimum is, it cannot be less than this bound.

#### $T^* \geq \frac{1}{m} \sum_j t_j$
- The total processing time is $\sum_j t_j$.
- One of $m$ machines must do at least $1/m$ fraction of total work.
- However, this lower bound is not strong enough.

#### $T^* \geq \max_j t_j$
- Some machine must process the most time-consuming job

>[!info] 2-Approximation
>Greedy-Balance produces an assignment of jobs to machines with makespan $T \leq 2 * T^*$

>[!note]
>In analyzing approximation algorithm, one compares the solution obtained to what one knows about the optimum. In this case, the lower bounds.

## Proof
Consider load $T$ of machine $M_i$ — machine $i$ attains the maximum load $T$ in our assignment.
- Let job $j$ be the last job scheduled on $M_i$
- $M_i$ had the smallest load of any machine.
- Its load just before this assignment is $T_i - t_j$ and since this is the smallest load, every other machine must have load at least $T_i - t_j$

Therefore, we have
>[!aside | right +++++]
>In other words $m(T_i - t_j)$ is the lower bound of the sum of loads on the machines
$$
\sum_k T_k \geq m(T_i - t_j) \implies T_i - t_j \leq \frac{1}{m}\sum_k T_k
$$

Note that the summation is the total load of all jobs, and so we can apply our lower bound:

$$
T_i - t_j \leq \frac{1}{m}\sum_k T_k \leq T^* \implies T_i - t_j \leq T^*
$$

Now when we assign the final job $j$, use the other lower bound and add them up.

$$
T_i = (T_i - t_j) + t_j \leq 2 T^*
$$

---

## Improved algorithm

**Longest Processing time** : Sort the jobs in decreasing order of processing time, and then, run list scheduling algorithm

```
LPT-List-Scheduling(m, n, t1, t2, ..., tn)
	Sort jobs so that t1 >= t2 >= ... >= tn

	for i = 1 to m {
		Li = 0.         // load on machine i
		J(i) = None     // jobs assigned to machine i
	}

	for j = 1 to n {
		i = argmin L_k  // smallest load machine
		J(i) += { j }   // assign job j to machine i
		Li += t_j       // update load of machine i
	}
```

### Observations
If we have at most $m$ jobs, then the greedy solution is clearly optimal since it puts job $j$ on its own machine.

>[!info] If there are more than $m$ jobs, then $T^* \geq 2 t_{m + 1}$

Consider the first $m + 1$ jobs. Since $t_j$ are in descending order, it must take at least $t_{m + 1}$ time
- There are $m + 1$ jobs and $m$ machines. By pigeonhole principle, at least one machine gets two jobs $\implies 2 t_{m+1}$

>[!info] The algorithm is 3/2 approximation algorithm $T \leq \frac{3}{2} T^*$

Consider $M_i$ with the maximum load. If $M_i$ holds a single job, then the schedule is optimal.

Suppose $M_i$ has at least two jobs, and let $t_j$ be the last job assigned to the machine. Since the jobs are sorted in descending order and $j$ comes after at least $m+1$ jobs,

$$
t_j \leq t_{m+1} \leq \frac{1}{2} T^*
$$

Now, similar to the previous proof,

$$
T_i \leq \frac{3}{3} T^*
$$


>[!caution]
>$\frac{3}{2}$ analysis is not a tight analysis


---

# Center selection problem
Select $k$ centers $C$ so that maximum distance from a site to the nearest center is minimized.

**Input**
Set of $n$ sites

**Distance function**
- `dist(s, s) = 0` 
- `dist(x, y) = dist(y, x)`
- `dist(x, y) <= dist(x, z) + dist(z, y)`

**Notation**
- `dist(s, C)` = $\min_{c \in C} \enspace dist(s, c)$
- $dist(s, C) \leq r$ for all sites $s \in S
- The minimum $r$ for which $C$ is an r-cover is the covering radius $r(C)$

**Goal**
Select a set $C$ of $k$ centers for which $r(C)$ is as small as possible

Repeatedly choose the next center to be the site farthest from any existing center

```
Greedy-Center-Selection(k, n, s1, s2, ... ,sn)
	C = None

	repeat k times
		Select a site si with maximum dist(si, C)
		Add si to C
	}
	return C
```

---
## Analysis

>[!info] Let $C^*$ be an optimal set of centers. Then $r(C) \leq 2 r(C^*)$

Suppose not. Let $r(C^*) \lt \frac{1}{2} r(C)$
- For each site $c_i$ in $C$, consider a radius $½ r(C)$ around it
- Exactly one $c_i^*$ in each radius; let $c_i$ be the site paired with $c_i^*$
- Consider any site $s$ and its closest center $c_i^*$ in $C^*$
- dist(s, C) ≤ dist(s, ci) ≤ dist(s, ci*) + dist(ci*, ci) ≤ 2r(C*).

Thus, $r(C) \leq 2r(C^*)$

>[!info] Greedy algorithm always places centers at sites, but is still within factor of 2 of best solution that is allowed to place centers anywhere

---

# Pricing method : Vertex cover

**Weighted vertex cover**
Given a graph $G$ with vertex weights, find a vertex cover of minimum weight

## Pricing method
Each edge must be covered by some vertex $i$. Each edge pays price $p_e \geq 0$ to use vertex $i$
- Think of each weights on the node as *costs*, $w_i$
- Think of each edge having to pay for its *share* of the cost of the vertex cover we find

The algorithm will not only find vertex cover $S$, but also determine prices $p_e \geq 0$ for each edge, so that if each edge pays the price $p_e$, this will in total approximately cover the cost of $S$

**Fairness** : Edges incident to vertex $i$ should pay $\leq w_i$ in total
- For each vertex $i$:
$$
\sum_{e=(i, j)} p_e \leq w_i
$$

>[!info] For any vertex cover $S$, and any fair prices $p_e$, $\sum_{e \in E} p_e \leq w(S)$

This is the lower bound on the cost of any solution.

Consider a vertex cover $S$. By definition of fairness, $\sum_{e=(i, j)} p_e \leq w_i$ for all nodes $i$ in $S$. Adding these inequalities over all nodes in $S$:

![[approximation-vertexcover.png| -s | -center]]

- Leftmost term: sum of terms, each of which s some edge price $p_e$
- Each edge $e$ contributes at least one term $p_e$ to the leftmost term
- It may contribute more than one copy of $p_e$ since vertex cover may include vertex from both sides
- Sum on the left hand side is at least as large as sum of all prices $p_e$

---

```
Weighted-Cover-Approx(G, w) 
	foreach e in E
		p_e = 0

	while there is an edge i-j such that neither i nor j is "tight"
		select such an edge e
		increase p_e without violating fairness

	S = set of all tight nodes
```

A node is *tight* if it is paid for $\sum_{e=(i, j)} p_e = w_i$

>[!caution]
>Note that the algorithm does not find the minimum-weight vertex cover

## Analysis

>[!info] Pricing method is a 2-approximation

In other words, the set $S$ and prices $p$ returned by the algorithm satisfy the inequality $w(S) \leq 2 \sum_{e \in E} p_e$

- All nodes in $S$ are tight $\sum_{e=(i, j)} p_e = w_i$ and add over all nodes in S:
  $w(S) = \sum_{i \in S} w_i = \sum_{i \in S} \sum_{e=(i,j)} p_e$
- An edge (i, j) can be included in the sum on the right hand side at most twice if i and j are both in $S$
  $w(S) = \sum_{i \in S} \sum_{e=(i,j)} p_e \leq 2 \sum_{e \in E} p_e$

Suppose that $S$ does not cover an edge i, j. This implies that neither $i$ nor $j$ is tight and this contradicts that the `while` loop terminated.

Combining the results above and the fairness lemma,

![[approximation-vertexcoverproof.png| -s |-center]]

---
# Integer Programming

Given integers $a_{ij}$ and $b$, find integers $x_j$ that satisfy
![[Screenshot 2023-11-18 at 12.20.44 PM.png | -m | -center]]

>[!example] Linear programming
>Suppose we wish to maximise $6x + 5y$ with the following:
>- **Objective function** : $6x + 5y$
>- **Decision variable** : $x, y$
>- **Constraints**: $x + y \leq 5 \space \text{and} \space 3x+ 2y \leq 12$
>  
>$\max(6x + 5y) \implies \max \begin{bmatrix} 6 \\ 5 \end{bmatrix} \cdot \begin{bmatrix} x && 5 \end{bmatrix} = \max \sum c_i x_i$
>Such that
>- $x + y \leq 5 \implies \sum x_i \leq 5$
>- $3x + 2y \leq 12 \implies \sum a_i x_i \leq 12$


# Weighted vertex cover
Given a graph $G = (V,E)$ with vertex weights $w_i \geq 0$, find a minimum weight subset of nodes $S$ such that every edge is incident to at least one vertex in $S$.

## Integer programming formulation
Let there be a *decision variable* $x_i$ for each node $v_i$.
- $x_i = 0$ if $v_i$ is not in the vertex cover
- $x_i = 1$ if $v_i$ is in the vertex cover

Then, we can have an $n$-dimensional vector $$\text{x} = \begin{bmatrix} x_i && ... && x_n\end{bmatrix}$$ corresponding to the decision variable.

For each edge $(i, j) \in E$, it must have one end in vertex cover, and this is denoted as an inequality:
$$
x_i + x_j \geq 1
$$

Then, denote the set of weights as an $n$-dimensional vector
$$\text{w} = \begin{bmatrix} w_i && ... && w_n\end{bmatrix}$$

We seek to minimise $\sum w_i x_i \implies w^{T}x$ — this is the *integer programming formulation*.

>[!info] Optimal value of *LP* $\leq$ optimal value of *ILP*

This is because LP is not equivalent to vertex cover.

This is a *lower bound* on the optimum in the form of a computable quantity for *LP*

## Rounding
>[!note]
>In linear programming formulation of weighted vertex cover, $x_i = \frac{1}{2}$ is possible.
>
>Therefore, we need to round.
>
>Given a fractional solution $x_i$, we define $S = \{i \in V : x_i \geq \frac{1}{2}\}$
## Analysis
>[!info] If $x^*$ is an optimal solution to LP then $S$ is a vertex cover

1. Consider an edge $(i, j)$.
2. At least $i$ or $j$ is in $S$
3. Since $x_i + x_j \geq 1$, in the solution to LP, either $x_i^* \geq ½$ or $x_j^* \geq ½ \implies$ either $i$ or $j$ will be placed in $x$

>[!info] The algorithm produces at most twice the minimum possible weight

1. Consider $w(S)$ of the vertex cover.
2. The set $S$ has vertices with $x_i^* \geq 1/2$ so the linear program paid for at least $½ w_i$ for node $i$
3. We have to pay $w_i$ which is at most twice as much

![[approx-vertexcoverLPrelaxation.png| -s | -center]]

---

# Generalised load balancing
Given a set of $m$ machines $M$ and a set of $n$ jobs $J$, assign jobs contiguously so that the maximum load on any machine is as small as possible.
1. Job $j$ can only run on a *restricted* set of machines $M_i \subseteq M$

## Formulation
We have the *integer linear programming* formulation
![[approx-loadbalancingIP.jpeg| -m | -center]]

### Relaxation
Then, we relax $x_ij \in \{0, t_j\}$ with $x_ij \geq 0$
![[approx-loadbalancingLP.png| -s | -center]]

>[!info] Let $L$ be the optimal value to $LP$, then the optimal makespan $L^* \geq L$

This is because LP has fewer constraints than IP formulation.

>[!info] The optimal makespan $L^* \geq \max_j t_j$

Some machine must process the most time-consuming job

## Rounding
LP may assign a small fractions of a job $j$ to each of the $m$ machines. Therefore, the algorithm can have a rounding of $x$ where each job $j$ is assigned to $i$ with $x_{ij} \gt 0$

Consider a bipartite graph $G(x) = (V(x) , E(x))$ where
- $V(x)$ the set of jobs and machines
- $E(x)$ : there is an edge *iff* $x_{ij} \gt 0$

>[!info] $G(x)$ is acyclic

For any solution to LP, we can obtain a new solution $x$ with the same load $L$ so that there are no cycles.

1. Root $G$ at some arbitrary machine node $r$
	1. If $j$ is a leaf node, assign $j$ to its parent machine $i$
	2. If $J$ is not a leaf node, assign $j$ to one of its children

![[approx-loadbalancingforest.jpeg| -m | -center]]

>[!info] Rounded solution only assigns to jobs with authorised machines

If job $j$ is assigned to $i$, then $x_{ij} \gt 0$, and LP solution can only assign positive value to authorised machines

## Analysis
>[!info] If job $j$ is a leaf node and machine $i$ is parent of $j$, then $x_{ij} = t_j$

Since $i$ is a leaf, $x_{ij} = 0$ for all other nodes except parent of $i$. LP constraint guarantees that $\sum x_{ij} = t_j$

>[!info] At most one non-leaf job is assigned to a machine

The only possible non-leaf job assigned to machine $i$ is if the job node is the parent of $i$.

>[!info] Rounded solution is 2-approximation

Let $J(i)$ be the jobs assigned to $m_i$

$L_i$ on machine $i$ has two components:
1. Leaf nodes
	![[approx-loadbalancingApprox.png| -m | -center]]
2. Parent(i)
	$t_{\text{parent}(i)} \leq L^*$


## Structure of solution

![[approx-loadbalancingstructure.jpeg| -s | -center]]

Solution to feasible flow problem with value $L$ are in 1-to-1 correspondance with $LP$ solutions of value $L$

### Finding acyclic solution
![[approx-loadbalancingnetworkflow.png| -m | -center]]

## Conclusion
==Running time== : Solving LP with mn + 1 variables

Can solve LP using flow techniques on a graph with $m + n + 1$ nodes.
Given $L$, find a feasible flow if it exists. Then, binary search to find $L^*$

---

# Knapsack problem

>[!note]- The problem
>![[Dynamic Programming#Knapsack problem]]

## NP-complete
The ==decision== version of the problem:

Given a finite set $X$, non-negative weights $w_i$, non-negative values $v_i$, a weight limit $W$, and a target value $V$, is there a subset $S \subseteq X$ such that:
$$
\sum_{i \in S} w_i \leq W
$$
$$
\sum_{i \in S} v_i \geq V
$$

#### Subset-Sum $\leq_p$ Knapsack

Given instance $(u_i, … , u_n , U)$ of Subset-sum, create Knapsack instance:


---

## DP II

### Optimal substructure
==Define== : $OPT(i, v)$ to be the minimum weight subset of items $1, … , i$ that yields a value *exactly* $v$.

**Case 1** : OPT does not select item $i$
- OPT selects best of $1, … , i-1$ that achieves exactly value $v$

**Case 2** : OPT selects item $i$
- Adds weight $w_i$ and need to yield exactly $v - v_i$
- OPT selects best of $1, …, i-1$ that achieves exactly value $v$

![[approx-knapsackdp2.png| -m | -center]]

### Analysis
==Running time== : $O(n V^*) = O(n^2 V_{\text{max}})$, where $V^*$ is the maximum value of $v$ such that $OPT(n, v) \leq W$.

Not polynomial in input size.

---

## Approximation
1. Round all values up to lie in smaller range
2. Run DP on the rounded instance
3. Return optimal items in rounded instance

### Rounding
Define
- $v_\max$ : largest value in the original instance
- $\epsilon$ : precision parameter
- $\theta$ = $\epsilon \frac{v_\max}{n}$

$$
\bar{v}_i = \lceil \frac{v_i}{\theta} \rceil \theta
$$
$$
\hat{v}_i = \lceil \frac{v_i}{\theta} \rceil
$$

>[!info] Optimal solution with either rounded values are equivalent.

![[approx-knapsackrounded.png| -m | -center]]

![[approx-knapsackApprox.png]]

---