We have ==algorithm design patterns== such as Greedy, Divide and conquer, DP. ==Algorithm design anti-pattern== are *NP-completeness*, *PSPACE-completeness* and *undecidability*.

- **NP-completeness** implies that polynomial time algorithm is unlikely.
- **Undecidability** implies that algorithm is not possible

---

# Polynomial time reduction
We need polynomial time algorithms to be able to solve in practice to be *retractable*.

| Yes                    | Probably No    |
| ---------------------- | -------------- |
| Shortest path          | Longest path   |
| Matching               | 3D-Matching    |
| Min cut                | Max cut        |
| 2-SAT                  | 3-SAT          |
| Planar 4-color         | Planar 3-color |
| Bipartite vertex cover | Vertex cover   |
| Primality testing      | Factoring      |

>[!note] Primality testing
>Given a number, identify if it is a prime or not

**Desiderata** Suppose we could solve *X* in polynomial time.

**Reduction** Problem $X$ *polynomial reduces to* problem $Y$ if arbitrary instances of problem $X$ can be solved using:
- Polynomial number of standard computational steps, **and**
- polynomial number of calls to oracle that solves problem $Y$

>[!aside | right +++++]
>*Oracle* is a computational model supplemented by special piece of hardware that solves instances of $Y$ in a single step

**Notation** $X \leq_{p} Y$

---

>[!info] Purpose
>Classify problems according to *relative* difficulty

If $X \leq_{p} Y$ and $Y$ cannot be solved in polynomial time, then $X$ **can** also be solved in polynomial time

If $X \leq_{p} Y$ and $X$ cannot be solved in polynomial time, then $Y$ **cannot** be solved in polynomial time

If $X \leq_{p} Y$ and $Y \leq_{p} X$, then $X \equiv_{p} Y$

---

# Reduction Strategies
## Reduction by Simple Equivalence

#### Independent set
Given a graph, $G = (V, E)$, and an integer $k$, is there a subset of vertices $S \subseteq V$ such that $|S| \geq k$ and for each edge at most one of its endpoints is in $S$?

![[reductability-setcover.png|80%]]
#### Vertex-Cover $\equiv_{p}$ Independent-set
>[!aside | right +++++]
>==Vertex cover== is a set $S$ of vertices of $G$ such that every edge of $G$ has at least one of member of $S$ as an endpoint.


Show that $S$ is an independent set $\iff$ $V - S$ is a vertex cover.

![[reductability-independetsetcover.png|50%]]
($\implies$)
1. Let $S$ be any independent set
2. Consider an arbitrary edge $(u, v)$
3. $S$ is independent $\implies$ $u \notin S$ **OR** $v \notin S \implies u \in V - S$ **OR**  $v \in V - S$
4. Thus, $V - S$ covers $(u, v)$

($\impliedby$)
1. Let $V - S$ be any vertex cover
2. Consider two nodes $u \in S$ and $v \in S$
3. Observe that $(u, v) \notin E$ since $V - S$ is a vertex cover
4. Thus, no two nodes in $S$ are joined by an edge $\implies$ S is an independent set
---
## Reduction from special case to general case
#### Set cover
Given a set $U$ of elements, a collection $S_1, S_2, … , S_m$ of *subsets* of $U$, and an integer $k$, does there exist a collection of $\leq k$ of these sets whose union equals to $U$?
![[reductability-vertexcover.png|80%]]
#### Vertex-cover $\leq_p$ Set-cover
>> Vertex-cover polynomial reduce to Set-cover

Given a *vertex-cover* instance $G = (V, E), \enspace k$ , we construct a *set cover* instance whose size equals the size of the vertex cover instance.

**Construction**
1. Create *set-cover* instance
	1. $U = E, S_v = \{ e \in E : \text{e incident to v}\}$
2. *Set-cover* of size $\leq k \iff$ vertex cover of size $\leq k$ 

![[reductability-vertexcovervssetcover.png|80%]]

---
## Reduction via gadgets
![[reductability-3sat.png|80%]]
#### 3-SAT $\leq_p$ Independent-set
>> 3-SAT polynomial reduces to Independent set

$G$ contains independent set of size $k = |\Phi| \iff \Phi$ is satisfiable

($\implies$)
- Let $S$ be independent set of size $k$
- $S$ must contain exactly one vertex in each triangle
- Set these literals to *true*
- Truth assignment is consistent and all clauses are satisfied

($\impliedby$)
- Given satisfying assignment, select one *true literal* from each triangle. This is an independent set of size $k$.

![[reductability-3satgraph.png|80%]]

---

**Transitivity applies**

In other words,
>> 3-SAT $\leq_p$ Independent-set $\leq_p$ Vertex-cover $\leq_p$ Set-cover

---
# Self-reducibility

1. **Decision** : Does there *exist* a vertex cover of size $\leq k$ ?
2. **Search** : *Find* vertex cover of *minimum* cardinality

>> Search problem $\leq_p$ decision

- This applies to all NP-Complete problems
- Justifies our focus on decision problem.

---

# Efficient certification and definition of NP
## Decision problem
- There is a contrast between finding a solution and checking a proposed solution

Let $X$ be a set of strings and $s$ an instance of a string.
$A$ solves problem $X$ : $A(s)$ = `yes` $\iff$ $s \in X$

$A$ runs in polynomial time if for every string $s$, $A(s)$ terminates in at most $p(|s|)$ steps where $p()$ is some polynomial.

## P
>[!info] Definition
>$P$ is the set of all decision problems for which there is a poly-time algorithm

## Efficient certification
$B$ is a efficient certifier for a problem $X$ if the following properties hold:
- $B$ is polynomial-time algorithm that takes two input arguments $s$ and $t$
- There is a polynomial function $p$ so that for every string $s$, we have $s \in X \iff$ there exists a string $t$ such that $|t| \leq p(|s|)$ and $B(s, t)$ = `yes`

>[!info] Certifier
>Algorithm $C(s,t)$ is a *certifier* for a problem $X$ if for every string $s, s \in X \iff$ there exists a string $t$ such that $C(s, t)$ = `yes` 

- Certification views things from *managerial* viewpoint → certifier does not determine whether $s \in X$ on its own. Rather, it checks a proposed proof $t$ that $s \in X$

## NP
>[!info] Definition
>Decision problems for which there exists a poly-time certifier.

NP stands for nondeterministic polynomial time.

>[!example]- Composite
>Given an integer `s`, is `s` composite?
>
>**Certificate** : A non-trivial factor $t$ of $s$. Note that such a certificate exists $\iff$ $s$ is a composite. Moreover, $|t| \leq |s|$
>
>**Certifier**
>```
>boolean C(s, t)
>	if (t ≤ 1 or t ≥ s)
>		return false
>	else if (s is a multiple of t)
>		return true
>	else
>		return false
>```
>
>Since we have a poly-time certifier, `COMPOSITES` is in NP

>[!example]- 3-SAT
>Given a CNF formula $\Phi$, is there a satisfying argument?
>
>**Certificate** : An assignment of truth values to the $n$ boolean variables
>
>**Certifier** : Check that each clause in $\Phi$ has at least one true literal
>
>**Conclusion** : SAT is in NP

>[!example]- HAM-CYCLE
>Given an undirected graph $G = (V, E)$, does there exist a simple cycle $C$ that visits every node?
>
>**Certificate** : A permutation of $n$ nodes
>
>**Certifier** : Check that the permutation contains each node in $V$ exactly once, and that there is an edge between each pair of adjacent nodes in the permutation
>
>**Conclusion** : HAM-CYCLE is in NP

---

## P, NP, EXP

#### $P \subseteq NP$
Consider any problem $X$ in $P$.
- By definition, there exists a poly-time algorithm $A(s)$ that solves $X$
- **Certificate** : $t = \epsilon$, certifier $C(s, t) = A(s)$
Here, the certifier ignores the proposed proof $t$ and simply solves the problem on its own. Since $A$ is polynomial, $C$ must also be polynomial.

#### $NP \subseteq EXP$
Consider any problem $X$ in $NP$
- By definition, there exists a poly-time certifier $C(s, t)$ for $X$
- To solve input $s$, run $C(s, t)$ for all strings $t$ with $|t| \leq p(|s|)$
- Return `yes` if $C(s, t)$ returns `yes` for any of these
---
# NP-complete

>[!info] Definition
>A problem $Y$ in $NP$ with the property that for *every* problem $X$ in $NP$, $X \leq_p Y$

Suppose $Y$ is an NP-complete problem. Then, $Y$ is solvable in poly-time $\iff$ P = NP.
- If P = NP, $Y$ can be solved in poly-time since $Y$ is in NP
- Suppose $Y$ can be solved in poly time.
	- Let $X$ be any problem in NP. Since $X \leq_p Y$, we can solve $X$ in poly-time. This implies that $NP \subseteq P$.
	- We already know that $P \subseteq NP$. Thus P = NP

## Circuit satisfiability
Given a combinational circuit built out of `AND, OR` and `NOT` gates, is there a way to set the circuit inputs so that the output is `1`?

>[!note]
>1. Circuit $K$ is a labeled, directed acyclic graph
>2. Sources in $K$ are labelled with either `1` or `0`
>3. Every other node is labelled with one of the boolean operators that have either one or two incoming edges
>4. There is a single node with no outgoing edge — the output

#### CIRCUIT-SAT is NP-complete
- Any algorithm that takes a fixed number of bits $n$ as input and produces a `yes` or `no` answer can be represented by such a circuit. Moreover, if algorithm takes poly-time, then circuit is of poly-size.

---

## Establishing NP-completeness
>[!info]
>If $X$ is an NP-complete problem, and $Y$ is a problem in NP with the property $X \leq_p Y$, then $Y$ is NP-complete.

Let $W$ be any problem in NP. Then $W \leq_p X \leq_p Y$
- First reduction by definition of NP-complete
- Second reduction by assumption

By transitivity, $W \leq_p Y \implies Y$ is NP-complete.

### 3-SAT
>[!info] 3-SAT is NP-complete

Suffices to show that CIRCUIT-SAT $\leq_p$ 3-SAT since 3-SAT is in NP.

Given an arbitrary instance of a CIRCUIT-SAT, we construct an equivalent instance of SAT in which each clause has exactly 3 variables.

1. Let $K$ be any circuit
2. Create a 3-SAT variable $x_i$ for each circuit element $i$
3. Make circuit compute correct values at each node. There will be 3 cases depending on the three types of gates:
![[np-circuitsat.png|50%]]
4. Hardcode the input values and the output value:
	1. $x_5 = 0$
	2. $x_0 = 1$
5. Turn clauses of length < 3 into clauses of length exactly 3

![[np-genres.png|80%]]

---
# Co-NP and asymmetry of NP

## Asymmetry of NP
The definition of efficient certification, and hence NP is *asymmetric* — we only need to have short proofs of `yes` instances

#### SAT vs TAUTOLOGY
- How to prove that a formula is not satisfiable?

#### NO-HAM-CYCLE
- How to prove that a graph is not Hamiltonian?

>[!info]
>Given a decision problem $X$, its complement $\bar{X}$ is the same problem with the `yes` and `no` answers inverse

Note that if $X \in P$ and $\bar{X} \in P$, we can simply run the algorithm and flip the answer. But this is not necessarily true for NP and cannot be worked around by simply inverting the output of the efficient certifier to solve the complementary problem

>> **If NP $\neq$ co-NP then P $\neq$ NP**

**Prove the contrapositive**

$P = NP \implies NP = co-NP$
- P is closed under complementation (solvable). Then, NP must be closed under implementation as well.

Starting from the assumption P = NP,
$$
X \in NP \implies X \in P \implies \bar{X} \in P \implies \bar{X} \in NP \implies X \in co-NP
$$
and
$$
X \in co-NP \implies \bar{X} \in NP \implies \bar{X} \in P \implies X \in P \implies X \in NP
$$

## Good characterizations
>[!note]
>$$ NP \cap \text{co-NP}$$
The problem $X$ with good characterization belongs to both P and NP.
- For `yes` instance, there is a succinct certificate
- For `no` instance, there is a succinct disqualifier


---

# Sequencing problems
## Hamiltonian Cycle
Given an undirected graph $G = (V, E)$, does there exist a simple *cycle* that contains every node in $V$?
![[np-hamcycle.png|50%]]
![[np-nonhamcycle.png|50%]]

## Directed hamiltonian cycle
Given a *digraph* $G= (V, E)$, does there exists a simple *directed cycle* that contains every node in $V$.

>> **DIR-HAM-CYCLE $\leq_{p}$ HAM-CYCLE**

Given a directed graph $G = (V, E)$, construct an undirected graph $G’$ with $3n$ nodes.
![[np-directedhamcycle.png|80%]]

$G$ has a Hamiltonian cycle $\iff$ $G'$ has a Hamiltonian cycle.

($\implies$)
1. Suppose $G$ has a directed Hamiltonian cycle
2. Then $G’$ has an undirected Hamiltonian cycle in the same order

($\impliedby$)
1. Suppose $G’$ has an undirected Hamiltonian cycle
2. In $G’$, the cycle must visit nodes in the order:
	- … RBGRBG … 
3. The $B$ in the cycle makes up the Hamiltonian Cycle in $G$ or the reverse of one.
---
>> **3-SAT $\leq_p$ DIR-HAM-CYCLE**

**Construction**
Given 3-SAT instance $\Phi$ with with $n$ variables $x_i$ and $k$ clauses,
- Construct $G$ to have $2^n$ Hamiltonian cycles
- Each path should have $2k$ nodes where $k$ is the number of clauses in the expression
![[np-3sat.png|80%]]

1. Add edges *left to right* on $P_i$ to correspond to the assignment $x_i$ = True
2. Add edges *right to left* on $P_i$ to correspond to the assignment $x_i$ = False
3. Inter-connect the paths by adding edge from one path to another at the endpoints
4. Add source and target nodes
5. Add backpath from target to source. Being the only path back to source, it will be always present in Hamiltonian Cycle
6. Add nodes corresponding to the clauses
7. If a clause $C_j$ contains $x_i$:
	1. Connect $C_j$ to $v_{i, 2j-1}, v_{i, 2j}$ from left to right if it contains $x_i$
	2. Connect $C_j$ to $v_{i, 2j-1}, v_{i, 2j}$ from right to left if it contains $\bar{x_i}$

### $\Phi$ is satisfiable $\iff$ $G$ has a Hamiltonian cycle

Suppose 3-SAT instance has satisfying assignment $x^*$
- Then, define Hamiltonian cycle as follows:
	- if $x^*_i$ = 1, traverse row $i$ from left to right
	- if $x^*_i$ = 0, traverse row $i$ from right to left
	- For each clause $C_j$, there will be at least one row $i$ in which we are going in *correct* direction to splice node $C_j$ into tour

Suppose there exists Hamiltonian cycle $H$ in $G$
- Any Hamiltonian Cycle in the constructed $G$ traverses $P_i$ either from *right to left* or *left to right*. This is because any path entering node $v_{i,j}$ has to exit either immediately or via one clause node in order to maintain Hamiltonian property.
- Since each path $P_i$ can be traversed in 2 possible ways and we have $n$ paths mapping to $n$ variables, there can be $2^n$ Hamiltonian cycles in the graph $G - \{ C_1, C_2, …, C_k \}$
- Each of the $2^n$ paths corresponds to a particular assignment for the variables $x_1, x_2, … , x_n$

## Traveling salesperson problem
Given a set of $n$ cities and a pairwise distance function $d(u, v)$, is there a tour of length $\leq D$?

**HAM-CYCLE**
Given a graph $G = (V, E)$, does there exist a simple cycle that contains every node in $V$?

#### HAM-CYCLE $\leq_p$ TSP
Given instance $G = (V, E)$ of HAM-CYCLE, create $n$ cities with distance function. We define $d(u, v) = 1$ if there is an edge in the HAM-CYCLE and define it to be 2 otherwise.

TSP instance has tour of length ≤ $n$ $\iff$ $G$ is Hamiltonian.

---

# Partitioning Problems

## 3-Dimensional matching
Given disjoint sets $X, Y, Z$, each of size $n$ and a set $T \subseteq X \times Y \times Z$ of triples, does there exist a set of $n$ triples in $T$ such that each element of $X \cup Y \cup Z$ is in exactly one of these triples?

### 3-SAT $\leq_p$ 3D-Matching
Given an instance $\Phi$ of 3-SAT, construct an instance of 3D-matching that has a perfect matching $\iff$ $\Phi$ is satisfiable.

**Construction**
- Create a gadget for each variable $x_i$ with $2k$ core and tip elements
- No other triples will use core elemets
- In gadget $i$, we must either use all the even triplets or the odd triplets
![[np-3dmatching.png| - s | -center]]
- For each class $C_j$, create two elements and three triplets
- Exactly one of these triples will be used in any 3D matching
- Ensures any 3D matching uses either odd or even
![[np-3dmatching3sat.png| -center]]
- For each tip, add a cleanup gadget  to cover the remaining tips

## Graph coloring
Given an undirected graph $G = (V, E)$, we seek to colour each node of $G$ such that if $(u, v)$ is an edge, $u$ and $v$ are assigned different colours.

>> Given a graph $G$ and a bound $k$, does $G$ have a $k$-coloring?

If $k = 2$, then it is the case of finding bipartite. $G$ is 2-colourable $\iff$ $G$ is bipartite

### 3-Color is NP-Complete
#### 3-Color is in NP
**Certificate** : $G$ and $k$
**Certifier** : Verify in polynomial time that
1. $k$ colors are used
2. No two nodes that share an edge have the same colour

#### 3-SAT $\leq_p$ 3-Color
Let there be an instance of 3-SAT with $n$ variables and $k$ clauses
- Define nodes $v_i$ and $\bar{v_i}$ to correspond to the variable $x_i$ and $\bar{x_i}$ respectively
- Join each pair $v_i$ and $\bar{v_i}$ by an edge and join both of these nodes to `Base`
- In any 3-colouring of $G$, the nodes $v_i$ and $\bar{v_i}$ must get different colours and both must be different from `Base`
- 

---
# NP-completeness

**P** = { problems solvable in polynomial time }
**NP** = { decision problems (answer is either yes or no) solvable in non-deterministic time } → can guess one out of polynomially many options in $O(1)$ time

3-SAT $\in$ NP because given a set of guesses for the literals, you can check in polynomial time whether it satisfies the CNF.


**NP** : Decision problems with poly-size certificates and poly-time verifiers for `yes` inputs

*Certificates* : the guesses

>[!note] NP-complete
>A problem $X$ is NP-complete if $X \in NP$ and $X$ is NP-hard.
>In other words, the problem is exactly as hard as everything in NP

>[!note] NP-hard
>$X$ is NP-hard if every problem $Y \in NP$ reduces to $X$ (ie it’s as hard as everything in NP. No harder than NP)
>
>$X$ is NP-hard $\implies$ $X \notin P$ unless $P = NP$

>[!note] Reduction
>Reduction from problem $A$ to problem $B$ is the poly-time algorithm converting $A$ inputs to *equivalent* $B$ inputs
>
>If $B \in P$ then $A \in P$
>If $B \in NP$ then $A \in NP$

#### How to prove $X$ is NP-complete
1. $X \in$ NP → Define what the *certificate* and *verifier* **OR** a non-deterministic algorithm
2. Prove that $X$ is NP-hard → reduce from some known $NP$-complete problem $Y$ to $X$

---
# Taxonomy of problems
## Packing problem
Given a collection of objects, choose $k$ objects. However, there is a set of conflicts that prevent you from choosing certain groups simultaneously.

## Covering problems
- Natural contrast to packing problems

Given a collection of objects, choose a *subset* that collectively achieves a certain goal.

## Partitioning problem
Involves a search over all ways to divide up a collection of objects into subsets so that each object appears in *exactly one of the subsets*.

## Sequencing problem
- Involves searching over a set of all permutations of a collection of objects.

## Numerical problems
Usually reduce to subset sum

## Constraint satisfaction
Consider basic satisfaction problems such as 3-SAT, CIRCUIT-SAT,
