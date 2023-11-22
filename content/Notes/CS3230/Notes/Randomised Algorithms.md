>[!caution]
>Linearity of expectation does not rely on independence


>[!note]
>Consider algorithms that behave randomly.
>Given the same worst-case input, the algorithm make random decisions as it processes the input.
>
>Efficient *deterministic* algorithms that always yield the correct answer are a special case of efficient *randomised* algorithms that only need to yield the correct answer with high probability


# Contention resolution
Suppose there are $n$ processes, $P_1, P_2, … , P_n$, each competing for access to a single shared database. If two or more processes access the database, all processes are locked out. Suppose the processes cannot communicate with one another at all.

## Randomised protocol
For some number $p > 0$, each process will attempt to access the database in each round with probability $p$.

- Exactly *one* process access the database → success
- Two or more try to access the database → locked out
- None try → round is wasted

==Symmetry breaking== paradigm makes the set of identical processes randomise its behaviour.

#### The probability that $i$ succeeds in accessing the database at time $t$ is $[ \frac{1}{en}, \frac{1}{2n}]$

Let $A[i, t]$ denote the event that $P_i$ attempts to access the database at time = $t$.
$$ Pr\Big[A[i, t]\Big] = p
$$
$$
 Pr\Big[\textlnot A[i, t]\Big] = 1 - Pr\Big[A[i, t]\Big] = 1 - p
$$
Let $S[i,t]$ denote the event that $P_i$ succeeds in accessing the database at time = $t$.
- $P_i$ attempts to access the database at round $t$
- Other processes do not attempt to access the database at $t$
- All processes are *independent*

$$
Pr\Big[ S[i, t] \Big] =  Pr\Big[A[i, t]\Big] \cdotp \prod_{j\neq i} Pr\Big[\textlnot A[j, t]\Big] = p(1-p)^{n-1}
$$
For $p$ value strictly between 0 and 1, find the derivative and when $p = \frac{1}{n}$, the maximum is achieved.
$$
Pr\Big[ S[i, t] \Big] = \frac{1}{n} \Big(1 - \frac{1}{n}\Big)^{n-1}
$$
>[!note]
>$\Big(1 - \frac{1}{n}\Big)^{n-1}$ converges monotonically from $[ \frac{1}{2}, \frac{1}{e}] \implies \frac{1}{en} \leq \frac{1}{n} \Big(1 - \frac{1}{n}\Big)^{n-1} \leq \frac{1}{2n}$

#### Upper bounds on failure
Let $Pr\Big[ F[i, t] \Big]$ denote the failure event that $P_i$ does not succeed in *any* of the rounds from 1 to $t$.

This is the intersection of the complementary *success* event from 1 to $t$.

From the [[Randomised Algorithms#The probability that $i$ succeeds in accessing the database at time $t$ is $[ frac{1}{en}, frac{1}{2n}]$ | previous claim]], the probability of failure can be at most $1- \frac{1}{en}$.

Then, we have
$$
Pr\Big[ F[i, t] \Big] \leq \Big( 1 - \frac{1}{en} \Big)^{t}
$$
Note that we can choose $t = \lceil en \rceil$ *(ceiling to make it an integer)*, 
$$
Pr\Big[ F[i, t] \Big] \leq \Big( 1 - \frac{1}{en} \Big)^{\lceil en \rceil} \leq \Big( 1 - \frac{1}{en} \Big)^{en} \leq \frac{1}{e}
$$
Now, choose $t = \lceil en \rceil \cdot (c \ln n)$
$$
Pr\Big[ F[i, t] \Big] \leq e^{-c \ln n} = n^{-c}
$$
Therefore,
- probability that $P_i$ has not succeeded after $\Theta(n)$ rounds is bounded by a constant
- probability that $P_i$ has not succeeded after $\Theta(n \ln n)$ rounds is bounded by an inverse polynomial *(very small)*

#### Bound on all processes succeeding
>[!note] Union bound
>Given events $e_1, … , e_n$
>
>$$
>Pr\Big[ \bigcup_{i=1}^{n} e_i \Big] \leq \sum_{i=1}^n Pr\Big[ e_i \Big]
>$$
>
>In simple terms, the union bound states that the probability of *at least one* of several events occurring is no greater than the sum of the individual probabilities of each event.

Let $F_t$ denote the event that the *protocol* fails after $t$ rounds (ie, there is a process that is yet to succeed)
- $F_t$ occurs $\iff$ one of $Pr\Big[ F[i, t] \Big]$ occurs

$$
F_t = \bigcup_{t=1}^{n}F\Big[i, t \Big]
$$

By *union bound*
$$
Pr[F_t] \leq \sum_{i=1}^n Pr\Big[ F[i, t] \Big]
$$
We want $F[i, t]$ to be as small as possible, and to do so, we can choose a value of $t$ is bounded by inverse polynomial to give the [[Randomised Algorithms#Upper bounds on failure | least bounded value]].

Choose $t = 2 \lceil en \rceil \ln n$,
$$
Pr[F_t] \leq n \cdot n^{-2} = \frac{1}{n}
$$
Therefore, the probability that *all* processes succeed within $2en \ln n$ rounds is at least $1 - 1/n$.

---
# Global minimum cut
Given a connected directed graph $G = (V, E)$, find a partition of $V$ into two non-empty sets $A$ and $B$ such that they have the minimum size.

>[!note]- s-t cut
>![[Max flow#Minimum cut problem]]

## Network flow solution
- Replace every edge $(u, v)$ with two anti-parallel edges $(u, v)$ and $(v, u)$
- Pick arbitrary node $s, t \in V$ and compute the $s-t$ min cut separating $s$ from each other vertex $t$

>[!caution]
>This is $n-1$ directed min-cut computations but can actually be calculated just as efficiently

## Contraction algorithm
>[!note]
>Randomised method for global min-cuts

Contraction algorithm works by choosing an edge $e$ at *random* and contracting it.![[IMG_53A448F55A23-1.jpeg | -m | -center]]
```
Pick an edge e uniformly at random
Contract edge e
	Replace u, v by a single super-node w
	Preserve edges, updating endpoints of u and v to w
	Keep parallel edges and delete self-loops
Repeat unitl graph has just 2 nodes, v1 and v2
Return the cut (all nodes that were contracted to form v1)
```

#### The contraction algorithm returns a min-cut with probability at least ${1}/{\binom{n}{2}} = 2 / n^2$

Consider a global min-cut $(A, B)$ of $G$ and suppose the size of min-cut is $k$. In other words, there are $k$ edges out of $A$ and $k$ edges into $B$. Let $F$ be the set of edges.

1. If an edge in $F$ were contracted, a node in $A$ and a node in $B$ will be in the same super node and $A, B$ will no longer be the output.
2. Therefore, we want to find the upper bound on probability that an edge in $F$ is contracted

We need to find a lower bound on the size of $E$.
1. If any node has degree less than $k$, $A, B$ will no longer be the min cut
2. Every node in $G$ has degree at least $k$ and so $|E| \geq ½kn$
3. Probability that an edge in $F$ is contracted $= \frac{k}{|E|} \leq \frac{2}{n}$

Let $\epsilon_1$ be the event that an edge is not contracted in iteration $i$.
1. After $i$ iterations, there are $n - i$ supernodes in the graph
2. at least $k$ edges incident to every supernode of $G$
Therefore, the probability that an edge in $F$ *is contracted* in the next iteration is **at most**
$$
\frac{k}{1/2k(n - i)} = \frac{2}{n - i}
$$

The cut $A, B$ will be returned if the algorithm did not contract any edges in $F$ in any of $n - 2$ iterations.

![[IMG_AB444D47FB7E-1.jpeg | -m | -center]]

The probability of failure is very high. Probability of success is amplified by running the algorithm many times.

#### Upper bound on failure
If we repeat the contraction algorithm $n^2 \ln n$ times with independent random choices, the probability of failing to find the global min-cut is at most $1/n^2$

![[Screenshot 2023-11-19 at 1.48.53 PM.png | -s | -center]]
---
# Max 3-SAT

>[!note]- The problem
>![[NP and Computational Intractability#3-SAT $ leq_p$ Independent-set]]

- Flip a coin, and set each variable `true` with probability $\frac{1}{2}$ independently for each variable.

#### Probability of clauses satisfied
Given a 3-SAT formula with $k$ clauses, the *expected number* of clauses satisfied by a random assignment is $\frac{7}{8}k$

- Probability of all 3 variables set to `false` = $\frac{1}{8}$
- Probability of any variable set to `true`, satisfying a clause = $1 - ⅛
= \frac{7}{8}$
- There are $k$ clauses $\implies \frac{7}{8} k$

>[!note]
>For any instance of 3-SAT, there exists a truth assignment that satisfies at least ⅞ of all clauses.

The probability a random assignment satisfies $\geq ⅞k$ clauses is at least $\frac{1}{8k}$

Let $p_j$ denote the probability that a random assignment satisfies exactly $j$ clauses.

Let $p$ be the probability that $\geq ⅞k$ clauses are satisfied.

![[Screenshot 2023-11-19 at 2.18.10 PM.png | -s | -center]]
Then, rearranging yields $p \geq \frac{1}{8k}$

## Analysis

### Johnson’s algorithm
Repeatedly generate random truth assignments until one of them satisfies at least $\frac{7k}{8}$ clauses.

#### Johnson’s algorithm is a ⅞-approximation algorithm
We know the probability of each iteration. The expected number of trials to find the satisfying assignment is at most $8k$.

---
# Universal Hashing

==Hash function== $h : U \rightarrow \{0, 1, … , n-1 \}$

==Hashing== : Create an array $H$ of size $n$. When processing element $u$, access array element $H[h(u)]$.

==Collision== : When $h(u) = h(v)$ but $u \neq v$
- A collision is expected after $\Theta(\sqrt{n})$ random insertions
- *Separate chaining* : $H[i]$ stores linked list of elements $u$ with $h(u) = i$