Arkar Kyaw Aung
A0234336J

---

>[!note]- Assignment questions
>> ![[private/Assignments/CS3230/Problem set 1]]

# Additional problems

Suppose there are `n` students and `m` tutorials.
Each student is matched to at most one tutorial. And, each tutorial has its own size limit; the $i$th tutorial can accept at most $s_{i}$ students for an integer $s_{i} \geq 0$.

Each student has a ranking of the tutorials in order of preference. Each tutorial has a ranking of the students in order of preference.

>[!caution] Definition of unstable
>Either $x$ is unmatched, or $x$ prefers $y$ to the current assignment for $x$.
>
>Either $y$ is not full, or $y$ prefers $x$ to one of the students currently assigned to $y$.

```plain-text
while there exists a student with no tutorial {
	choose such a student s
	y = 1st class on s's list to whom s has not applied

	if (y is not full) {
		enroll in class
	}
	else if (y is full and y prefers s over lowest ranked stundet, s', enrolled) {
		enroll y and set s' to be free
	} else {
		y rejects s
	}
}
```





