#notes #cs3230

# Definition of ==stable==

a matching is stable _when there does not exist any pair (A, B) which both prefer each other to their current partner_ under the matching.

--- 

## Example Problems

Matchmaker must match men and women. Each man ranks all the women, and each woman ranks all the men. How to pair them up?  
	
`input` : Preference rankings for all `n` men and all `n` women
`output`: a Stable matching
*Design an algorithm that is correct and also runs [[Basics of algorithm analysis | fast]]*

Consider the preference rankings

```start-multi-column
ID: ID_zccn
Number of Columns: 2
Largest Column: standard
Border: off
Shadow: off
```

|             |          |         |      |
| ----------- | -------- | ------- | ---- |
| **Anish**   | Xinyu    | Yashoda | Zuzu |
| **Bao**     | Yashoday | Xinyu   | Zuzu |
| **Charlie** | Xinyu    | Yashoda | Zuzu |

--- column-end ---

|             |       |       |         |
| ----------- | ----- | ----- | ------- |
| ==Xinyu==   | Bao   | Anish | Charlie |
| ==Yashoda== | Anish | Bao   | Charlie |
| ==Zuzu==    | Anish | Bao   | Charlie |


--- end-multi-column

**Unstable**: `(Anish, Zuzu)`, `(Bao, Yashoda)`, `(Charlie, Zuzu)`
**Stable**: 
	`(A, Y)`, `(B, X)`, `(C, Z)`
	`(A, X)`, `(B, Y)`, `(C, Z)`

>[!note] Blocking pair
>Given a matching `M`, a pair `(m, w)` is a ==blocking pair== for `M` if `(m, w)` $\notin$ `M` and `m` prefer `w` to its current partner in `M` **and** `w` prefers `m` over its current partner in `M`

---

## Approach

>> Start with any matching. Keep identifying ==rogue== couples and match them with each other.

#### **Gale-Shapley algorithm**

``` plain text
initialise each person to be free

while (some man is free and has not proposed to every woman) {
	choose such a man m
	w = 1st woman on m's list to whom m has not yet proposed

	if (w is free)
		assign m and w to be engaged
	else if (w prefers m to her fiance m')
		assign m and w to be engaged, and m' to be free
	else
		w rejects m
}

```

---

## Observations
- Seems to output a stable matching
- Outputs the *same* stable matching

---

#### 🚦 Gale-Shapley terminates

> [!note]
> The `while` loop in Gale-Shapley runs ≤ $n^2$ times.


1. A `man` never proposes to the same `woman` twice and each `while` loop makes a new proposal
2. There are $n^2$ possible proposals.

Therefore, the number of loop iterations cannot be more than $n^2$.

---

#### ⬇️ Men propose to women in decreasing order of preference
Consider a man `m`. Through the course of the algorithm, he may sometimes be engaged, and sometimes be free. But since he always propose to the highest-ranked woman in his list, he keeps going down the list.

---

#### 💃 Women’s partners keep getting better
Consider a woman `w`. Once she gets engaged, the algorithm may only change her partner but never sets her free. She only changes her partner if her preference is ranked higher.

---

#### 💍 Upon termination, each man is engaged to a unique woman
**Proof by contradiction**
Suppose `m` is free at termination, but then there is also a woman `w` who is also free.
By [[#⬇️ Men propose to women in decreasing order of preference | previous lemma]], `w` never have been proposed to. This is impossible as `m` must have proposed to `w`. ==Contradiction==

---

#### 🐎 Output is stable
**Proof by contradiction**
Suppose the matching is not stable. In other words, there is a pair `(m, w)` such that they prefer each other over their current partners.

Consider the couple `(m' , w)` and `(m, w')` such that `(m, w)` prefer each other over their current partners.

For current pairs to exist, `m` must have proposed to `w'` first before `w` as he proposes to woman of [[#⬇️ Men propose to women in decreasing order of preference | decreasing order of preference]].

When `w` rejects `m`, it must be because there exists another man, `m'` whose preference ranks higher, as [[#💃 Women’s partners keep getting better | women’s partner keeps getting better]]. ==Contradiction==.

---

>[!note] Men-optimality
>Gale-Shapley returns the matching in which each man `m` is paired with `best(m)`.
>
>Here, `best(m)` is the highest woman ranked on his list who could be his partner in some stable matching. This also suggests that no two men will have `best(m)`.

>[!note] Women-pessimility
>In men-optimal stable matching with Gale-Shapley, each woman `w` is paired with `worst(w)`.

---