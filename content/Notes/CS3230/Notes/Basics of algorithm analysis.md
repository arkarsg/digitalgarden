>[!quote] What is an algorithm?
>A *finite sequence* of *well-defined instructions* to solve a given computational problem.

>[!aside | right +++++]
>There are many different metrics of efficiency but the primary objective is the running time.


→ How then do we design an ==efficient== algorithms — measured by its running time?

---

# Running time
Notice that the running time is ==machine dependent== and ==output dependent==.

- [i] Perform ==mathematical analysis== of the algorithm.

## Word-RAM model
A *model of computation* where only ==RAM== and ==CPU== is considered. 


![[wordrammodel.png| -m | -center]]

- Word is the ==basic storage== unit of RAM. Word is a collection of few bytes.
- Each input item is stored in ==binary format==
- RAM can be viewed as a huge array of words
- Any location of RAM can be accessed in the same time irrespective of location
- Data as a program fully resides in the RAM
- Each arithmetic operation or logical operation involving a ==constant number of words== takes ==constant number of cycles (steps)== by the CPU.

>[!note] Measuring (mathematical) running time
>- Number of instructions take in word-RAM model

---

# Example problems

Consider $F(0) = 0$,  $F(1) = 1$ and $F(n) = F(n-1) + F(n-2)$ for $n > 1$.

Given `n` and `m`, compute `F(n) mod m`.

## Recursive approach

```plain text
FibRecursive(n, m) {
	if n = 0 return 0
	if n = 1 return 1
	else return (FibRecursive(n - 1) + FibRecursive(n-2)) mod m);
}
```

Number of instructions ≥ $2^\frac{n-2}{2}$

## Iterative approach
```plain text
IFIB(n,m) {
	if n=0 return 0;
		else if n=1 return 1;
		else {       
			a ß 0;   bß 1;
			For(i=2 to n) do {
				temp ß b; 
				bß (a+b) mod m;
				aß temp;
			}

		}

	return b;
}
```

No. of instructions ≤ $5n$

---

# Polynomial time
### Brute force
For many non-trivial problems, there is a natural brute force search algo that checks for every possible solution.

>[!aside | right +++++]
>$n!$ for [[Stable Matching]] with $n$ men and $n$ women.

However, it takes $2^N$ time or worse for inputs of size $N$, which is unacceptable in practice.

>[!note] Desirable scaling property
>When the input size doubles, the algo should only slow down by some constant factor `C`.

>[!quote]
>An algorithm is ==poly-time== if the above scaling property holds.

>[!note] Worst-Case polynomial time
>An algorithm is efficient if its running time is polynomial.
>
>There exists constants `c > 0` and `d > 0` such that on every input of size `N`, its running time is bounded by `c N^d` steps

---

# Worst-case analysis

## Worst case running time
>[!aside | right +++++]
>Draconian view. Strong guarantee that there is no adversary that will make the algorithm run for a very long time.

>[!note]
>Obtain bound on largest possible running time of algo input of a given size `N`.

## Average case running time
>[!note]
>Obtain bound on running time of algorithm of ==random== input as a function of input size `N`.

However, this is hard to accurately model real instances by random distributions and algorithms tuned for certain distribution may perform poorly on other inputs.

This requires knowledge of input distribution.

---

# Asymptotic order of growth
>[!caution]
>When we say an algorithm is more efficient than another, we are comparing ==asymptotically large values of input size==.

>[!quote] Definition
>To compare running time of two different algorithms we see which is more efficient (or fast) for *large inputs* in the ==worst case==.

>> Suppress constant factors and lower order terms.

### Upper bound
>[!note] Definition
>`T(n)` is `O(f(n))` if there exists constants $c > 0$ and $n_0 ≥ 0$ such that for all $n ≥ n_0$ we have `T(n)` ≤ $c \times f(n)$.

### Lower bound
>[!note] Definition
>`T(n}` is $\Omega(f(n))$ if there exists constants $c ≥ 0$ and $n_{0} ≥ 0$ such that for all all $n ≥ n_0$ we have `T(n)` ≥ $c \times f(n)$.


### Tight bound
>[!note] Definition
>`T(n}` is $\Theta(f(n))$ if `T(n)` is both $O(f(n))$ and $\Omega(f(n))$

## Notation
Suppose T(n) = O(f(n)).

Note that it is ==asymmetric==.
$$ \begin{gathered} f(n) = 5n^3, \space g(n) = 3n^2 \\ f(n) = O(n^3) = g(n) \\ \textsf{but} \space f(n) \neq g(n) \end{gathered} $$

Instead, use

$$ T(n) \in O(f(n)) $$

>[!caution] Use the proper bound
>It is meaningless to say that an algorithm is *at least O(n log n)* comparisons. Instead, use $\Omega$ for lower bounds.


## Properties

>[!note]
>This applies for lower, upper and tight bounds.

### **Transitivity**

>> If $f = O(g)$ and $g=O(h)$ then, $f = O(h)$

---

### **Additivity**

>> If $f = O(h)$ and $g=O(h)$ then $f + g = O(h)$


---

# Common confusions

$$ 2^{n+5} = 2^5 \cdot 2^n = O(2 ^ n) $$

But,

$$ 2^{5n} \notin O(2^n) $$

---

$$ max(f(n), g(n)) = \Theta(f(n) + g(n)) $$