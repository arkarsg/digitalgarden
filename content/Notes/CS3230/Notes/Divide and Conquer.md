>> ==Divide== the problem into a number of subproblems that are smaller instances of the same problem
>> ==Conquer== the subproblems by solving them recursively
>> ==Combine==  the solutions to the subproblems into the solution for the original problem.

---

## Tower of Hanoi
- There exists a solution for the `n-1` discs to move from the first peg to the second peg
- Then, you can move the `n-1` discs from the second peg to the third peg
```plain-text
Hanoi(n, src, dst, tmp) {
	if n > 0 {
		Hanoi(n-1, src, tmp, dst)
		move disk n from src to dst
		Hanoi(n-1, tmp, dst, src)
	}
}
```

>[!caution]
>Use induction to prove correctness that you can move `n-1` from first peg to middle peg.
>
>Do not try to *unroll* recursion — it will not give you any intuition

---

## Most common usage
- Break up problem of size `n` into two equal parts of size `½ n`
- Solve the 2 parts recursively
- Combine 2 solutions into overall solution in ==linear time==

- Brute force will be $O(n^2)$
- Divide and conquer is usually $O(n log n)$

---

# Mergesort

1. Divide the array into two halves
2. Recursively sort each half
3. Merge two halves to make sorted whole

>[!aside | right +++++]
>Note that the `sort` step is a recurrence relation

![[mergesort.png|80%]]

### Merging in linear time
>[!note] Merging
>Combine two pre-sorted lists into a sorted whole

Usually, we wish to merge efficiently in linear time.

- Keep track of smallest element in each sorted half
- Insert smallest of two elements into ==auxiliary array==
- Repeat until done

---

# Analysing the running time

>[!aside | right +++++]
>Note that there is an implicit assumption that we are using the *worst case* (ie, the maximum number of comparisons)

Let $T(n)$ be the number of *comparisons* to mergesort an input of size n.

Then, we have the *recurrence relation*:

![[mergesortrecurrence.png|80%]]

Therefore, we have $T(n) = O(n \log_2 n)$

---
## Proof by recursion tree
First, assume that $n$ is a power of 2

![[recursiontree.png|80%]]

- Note that the overhead cost at each level stays the same
---

## Proof by induction
1. Base case: $n = 1$
2. Inductive hypothesis: $T(n) = n \log_2 n$
3. Goal: show that $T(2n) = 2n \log_2 (2n)$

![[recurrencerelation.png|50%]]

---

With induction, we can also show that the recurrence relation applies where $n$ is not a power of 2, that is
$$
T(n) \leq n \lceil{\lg n}\rceil
$$

---

# Counting inversions

## Similarity metric
>[!note]
>Number of inversions between two rankings

Suppose we have rank : {1, 2, … , n}
and another rank : {a_1, a_2, …, a_n}
Then, two objects are inverted if $i < j$ but $a_i > a_j$

The more the number of inversions, the less similar the two rankings are.

![[inversions.png|80%]]

## Approach

1. ==Divide== : Separate list into two pieces → $O(1)$
2. ==Conquer== : Recursively count inversions in each half → $2T(\frac{n}{2})$
3. ==Combine== : Count inversions where $a_i$ and $a_j$ are in different halves
---

### Divide
![[inversionsdivide.png|80%]]

### Conquer
![[inversionsconquer.png|80%]]

### Combine

>> How to count *blue-green* inversions?

- Assume each half is ==sorted==
- Count inversions where $a_i$ and $a_j$ are in different halves
- Merge 2 sorted halves into sorted whole

![[inversionsmerge.png|80%]]

---

==Pre-condition== : `Merge-and-count` → A and B are sorted
==Post-condition== : `Sort-and-count` → L is sorted

```plain-text
Sort-and-Count(L) {
	if list L has one element
		return 0 and the list L

	Divide the list into two halves A and B
	r_a, A = sort-and-count(A)
	r_b, B = sort-and-count(B)
	r, L = merge-and-count(A, B)
	return r_a + r_b + r, L
}
```
---

# Closest pair of points

Given $n$ points in the plane, find a pair with smallest *euclidean* distance between them.

Brute force : ==$\Theta (n^2)$==
1D version : ==$O(n \log n)$==

**Assume** that no points have same $x$ coordinates for clearer representation.

## Approach

1. ==Divide== : Sub-divide region by drawing a vertical line such that there are $\frac{1}{2} n$ points on each side
2. ==Conquer== : Find closest pair in each side recursively
3. ==Combine== : Find closest pair with one point in each side

→ Return best of 3 solutions

![[shortestdistance.png|80%]]

---
>> How to find closest pair with one point in each side?

Let $\delta = \min(12, 21)$.
Then, we find the closest pair with one point in each side assuming that distance < $\delta$.

- [i] To find points < $\delta$, we only need to consider points in the strip $[L - \delta, L + \delta \space]$

>[!note] Define
> Let $s_i$ be the point in the 2$\delta$ strip with the $i$-th smallest $y$-coordinate.

**Claim** : If $| i - j | \geq 12$, then the distance between $s_i$ and $s_j$ is at least $\delta$.

1. No 2 points lie in the same $\frac{1}{2}\delta \times \frac{1}{2}\delta$ box → otherwise they will have distance less than $\delta$
2. Two points at least 2 rows apart have distance ≥ $\delta$

Therefore, we do not need to check every points within the strip, but only the next 11 neighbours.

```plain-text
Closest-Pair(p1, ..., pn) {  
	Compute separation line L such that half the points are
	on one side and half on the other side.

	delta_1 = Closest-Pair(left half)
	delta_2 = Closest-Pair(right half)
	delta = min(delta_1, delta_2)

	Delete all points further than delta
	from separation line L

	Sort remaining points by y-coordinate.

	Scan points in y-order and compare distance between each
	point and next 11 neighbors.
	If any of these distances is less than delta, update
	delta.

return delta
}
```

### Running time

$$ T(n) \leq 2T(\frac{n}{2}) + O(n \log n) \implies T(n) = O(n \log^2 n)
$$

To improve the running time, instead of sorting points by $y$-coordinate in each recursive call, maintain all points sorted by $y$-coordinate and all points sorted by $x$-coordinate.

$$ T(n) \leq 2T(\frac{n}{2}) + O(n) \implies T(n) = O(n \log n) $$

---

# Matrix multiplication


# Master theorem

![[Master theorem.jpeg|80%]]
