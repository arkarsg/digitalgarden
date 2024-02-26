# Interval scheduling
Job $j$ starts at $s_j$ and finishes at $f_j$ and two jobs are compatible if they do not overlap.

**Goal**: find maximum subset of mutually compatible jobs.

>[!note] Greedy approach
>Consider jobs in some order. Take each job provided it is compatible with the ones already taken.

There are different heuristics to the order of the jobs:
- Earliest start time
- **Earliest finish time**
- Shortest interval
- Fewest conflicts

However, not all of them work to give the optimal solution (give counter example).

```plain-text
Sort jobs by finish time

A <- {}
for j = 1 to n {
	if (j is compatible with A) {
		A += j
	}
}

return A
```

>[!note] Implementation
>$O(n \log n)$
> - Remember job $j$ that was added last to A
> - Job $j_next$ is compatible with $A$ if start time of $j$ is greater than the finish time of the last added job, $j$.

#### Greedy algorithm is optimal

**By contradiction**
1. Assume that greedy approach is not optimal.
2. Let $i_1, i_2, …, i_k$ denote set of jobs selected by greedy.
3. Let $j_1, j_2, …, j_m$ denote set of jobs in the solution with $i_1 = j_1, i_2 = j_2, …, i_r = j_r$ for the largest possible value of $r$
4. It is possible to modify the optimal solution such that it matches the greedy solution

>[!note]- General form of proof
> _Claim:_ Let 𝑆 be the solution output by the algorithm and 𝑂 be the optimum solution. If 𝑆 is different from 𝑂, then we can tweak 𝑂 to get another solution 𝑂∗ that is different from 𝑂 and strictly better than 𝑂.
> 
> Notice why this is useful. If the claim is true, it follows that the algorithm is correct. This is basically a proof by contradiction. Either 𝑆 is the same as 𝑂or it is different. If it is different, then we can find another solution 𝑂∗ that's strictly better than 𝑂 -- but that's a contradiction, as we defined 𝑂 to be the optimal solution and there can't be any solution that's better than that. So we're forced to conclude that 𝑆 can't be different from 𝑂; 𝑆 must always equal 𝑂, i.e., the greedy algorithm always outputs the correct solution. If we can prove the claim above, then we've proven our algorithm correct.
> 
> Fine. So how do we prove the claim? We think of a solution 𝑆 as a vector (𝑆1,…,𝑆𝑛) which corresponds to the sequence of 𝑛 choices made by the algorithm, and similarly, we think of the optimal solution 𝑂 as a vector (𝑂1,…,𝑂𝑛) corresponding to the sequence of choices that would lead to 𝑂. If 𝑆 is different from 𝑂, there must exist some index 𝑖 where 𝑆𝑖≠𝑂𝑖; we'll focus on the smallest such 𝑖. Then, we'll tweak 𝑂 by changing 𝑂 a little bit in the 𝑖th position to match 𝑆𝑖, i.e., we'll tweak the optimal solution 𝑂 by changing the 𝑖th choice to the one chosen by the greedy algorithm, and then we'll show that this leads to an even better solution. In particular, we'll define 𝑂∗ to be something like
> 
> 𝑂∗=(𝑂1,𝑂2,…,𝑂𝑖−1,𝑆𝑖,𝑂𝑖+1,𝑂𝑖+2,…,𝑂𝑛),
> 
> except that often we'll have to modify the 𝑂𝑖+1,𝑂𝑖+2,…,𝑂𝑛 part slightly to maintain global consistency. Part of the proof strategy involves some cleverness in defining 𝑂∗ appropriately. Then, the meat of the proof will be in somehow using facts about the algorithm and the problem to show that 𝑂∗ is strictly better than 𝑂; that's where you'll need some problem-specific insights. At some point, you'll need to dive into the details of your specific problem. But this gives you a sense of the structure of a typical proof of correctness for a greedy algorithm.


---

# Interval partitioning

>[!note] Goal
>Find the minimum number of classrooms to schedule all lectures so that no 2 occur at the same time in the same room.

#### **Depth**
The depth of a set of open intervals is the maximum number that contain any given time.

Consider lectures in increasing order of *start time* → assign lecture to any compatible classroom.

```plain-text
sort intervals by starting time so that it is in non-decreasing order
d = 0 (number of allocated classrooms)

for j = 1 to n {
	if lecture j is compatible with some classroom k
		schedule lecture j in classroom k
	else
		allocate new classroom d + 1
		schedule lecture j in classroom d + 1
		d += 1
}
```

>[!note] Implementation
>$O(n \log n)$
>- For each classroom k, maintain the finish time of the last job added.
>- Keep the classrooms in a priority queue

### Observations
>> Greedy algorithm never schedules two incompatible lectures in the same classroom
#### Greedy algorithm is optimal
1. Let $d$ = number of classrooms that the greedy algorithm allocates
2. Classroom $d$ is opened because we needed to schedule a job that is incompatible with all $d-1$ classrooms.
3. Since we sorted by *start time*, all these incompatibilities are caused by lectures that start no later than $s_j$
4. Thus, we have $d$ lectures overlapping at time $s_j + \epsilon$

---

# Scheduling to minimise lateness

Suppose there is a single resource that processes one job at a time. That is, job *j* requires $t_j$ units of processing time and is due at time $d_j$.

If *j* starts at time $s_j$, then it finishes at $f_j = s_j + t_j$

**Lateness** : $l_j = \max{\{0, f_j - d_j\}}$

>> How do we schedule all jobs to minimise ==maximum== lateness $L = \max{l_j}$

### Greedy approach
Consider jobs in some order
- Shortest processing time first (ascending order of $t_j$)
**Counter example**

|       | 1   | 2   |
| ----- | --- | --- |
| $t_j$ | 1   | 10  |
| $d_j$ | 100 | 10  |




- Earliest deadline first (ascending order of $d_j$)
==Works==
- Smallest slack (ascending order of $d_j - t_j$)
**Counter example**

|       | 1   | 2   |
| ----- | --- | --- |
| $t_j$ | 1   | 10  |
| $d_j$ | 2 | 10  |

---

```plain-text
sort n jobs by deadline so that the deadlines are in non-decreasing order

t = 0
for j=1 to n
	assign job j to interval [t, t+t_j]
	s_j = t, f_j = t + t_j
	t = t+t_j
output intervals [s_j, f_j]
```

---
### Observations

>> There exists an optimal schedule with no *idle time*

#### The greedy schedule has no idle time


#### Greedy schedule has no inversions
>[!note] Inversions
>An *inversion* in schedule *S* is a pair of jobs *i* and *j* such that *i* < *j* but j is scheduled before i.

**Claim** : Swapping two adjacent, inverted jobs reduces the number of inversions by one and does not increase the max lateness

![[inversion.png|80%]]
![[greedyinversion.png|80%]]

#### Greedy schedule S is optimal

Define S* to be an optimal schedule that has the fewest number of inversions.
1. Assume S* has no idle time
2. If S* has no inversions then, S = S*
3. If S* has an inversion, let i-j be an adjacent inversion
	- Swapping i and j does not increase the maximum lateness and strictly decreases the number of inversions
	- This contradicts the definition of S*

---

## Strategies in greedy analysis

1. **Greedy algorithm stays ahead** : After each step of the greedy algorithm, its solution is at least as good as any other algorithm
2. **Exchange argument** : Note that this is the general form of proof to show the optimality of greedy algorithm. Gradually transform any solution to the one found by the greedy algorithm without hurting its quality
3. **Structural** : Discover a simple structural bound asserting that every possible solution must have a certain value. Then show that your algorithm always achieves this bound.

---

# Optimal caching

>[!caution] Caching
>In this section, we consider an ==offline cache==, where the sequence of requested items are known.

**Goal** : ==Eviction schedule== that minimises number of cache misses

## Furthest-in-future
>[!note] Eviction policy
>Evict item in the cache that is not requested until farthest in the future. This is the optimal eviction schedule.

A *reduced* schedule is a schedule that only inserts an item into the cache in a step in which that item is requested. We can transform an *unreduced* schedule into a *reduced* schedule with no more cache misses.

**Proof**
1. Suppose S brings *d* into the cache at time *t*, without a request.
2. Let *c* be the item S evicts when it brings *d* into the cache.

Then, we have the following:
1. *d* evicted at time *t’*, before the next request for *d*
2. *d* requested at time *t’*, before *d* is evicted


```start-multi-column
ID: ID_8xo5
Number of Columns: 2
Largest Column: standard
Border: off
Shadow: off
```

#### Case 1
![[unreducedtoreducedcache.png|80%]]

--- column-end ---

#### Case 2
![[unreducedtoreducedcache2.png|80%]]

--- end-multi-column

### Optimality

>> The eviction policy is the optimal eviction algorithm

**Proof**

>[!note] Invariant
>There exists an optimal reduced schedule $S$ that makes the same eviction schedule as $S_{ff}$ through the first $j + 1$ requests

Let $S$ be reduced schedule that satisfies invariant through $j$ requests. We produce $S’$ that satisfies invariant after $j + 1$ requests.

1. Consider $(j+1)$st request $d = d_{j+1}$
2. Since $S$ and $S_{ff}$ have agreed up until now, they have the same cache contents before request $j+1$
3. **Case 1**: $d$ is already in cache → $S’ = S$ satisfies invariant
4. **Case 2**: $d$ is not in the cache and $S$ and $S_{FF}$ evict the same element → $S = S’$ satisfies invariant
5. **Case 3**: $d$ is not in the cache and $S_{FF}$ evicts $e$; $S$ evicts $f \neq e$

![[ff_eviction.png|80%]]

---

# Examples

## Greedy stays ahead
>[!tip] The question
>Suppose you are hiking along the path, only in the day. Each time you come to a potential stopping point, determine whether they can make it to the next one before nightfall. Prove that greedy stays ahead in minimising the number of stops needed.

- Represent the trail as a line segment $L$
- Assume that the potential stopping points are located at distances $x_1, x_2, … , x_3$ from the start of the trail.
- A set of stopping points is *valid* if the distance between each adjacent pair is at most $d$

Suppose there exists some optimal solution $O$. 

Let $R = \{x_{p1}, … , x_{pk}\}$ denote the set of stopping points chosen by the greedy algorithm, and suppose by way of contradiction that there is a smaller set $S = \{x_{q1}, …, x_{qm}\}$, with $m < k$

To show that greedy algorithm stays ahead, show that stopping point reached by the greedy algorithm on each day $j$ is farther than the stopping point reached under the alternate solution.

>> For each $j = 1, 2, … ,m$, we have $x_{pj} \geq x_{qj}$

**Base case**
When $j=1$, this is true as we travel as long as possible before stopping.

Let $j > 1$ and assume that the claim is true for all $i < j$. Then,
$$x_{qj} - x_{q_{j-1}} \leq d$$
since $S$ is a valid set of stopping points and
$$ x_{q_j} - x_{p_{j-1}} \leq x_{q_j} - x_{q_{j-1}} $$
since $x_{p_{j-1}} \geq x_{q_{j-1}}$ by the induction hypothesis.

Combing the two inequalities, we have
$$
x_{q_j} - x_{p_{j-1}} \leq d
$$

which suggests that $x_pj$ is farther along than $x_qj$

Our earlier statement implies in particular that $x_qm$ ≤ $x_pm$ . Now, if $m < k$, then we must have $xpm < L − d$, for otherwise your friends would never have needed to stop at the location $xpm+1$. Combining these two inequalities, we have concluded that $xqm < L − d$; but this contradicts the assumption that S is a valid set of stopping points.

Consequently, we cannot have $m < k$, and so we have proved that the greedy algorithm produces a valid set of stopping points of minimum possible size.

---

