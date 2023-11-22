In predicate logic (or first order logic), it consists of formulae built from *predicate* (lower case), *operators* $(=, \leq \text{etc})$, *constants* (lower case), *variables* (upper case, quantified or free), *connectives*, and quantifiers $(\forall, \exists)$ 

---
>[!note] The existential qualifier
>The existential qualifier is a generalisation of disjunction
>$\exists{X} F[X] \equiv F[a] \lor F[b] \lor ...$

>[!note] The universal quantifier
>The universal quantifier is a generalisation of conjunction
>$\forall{X} F[X] \equiv F[a] \land F[b] \land ...$

---

#  Relational Calculus

In DRC, variables range over values of fields of tables (ie they range over domains). Domain relational calculus is the theoretical basis of *Query by example*.

In ==Tuple Relation Calculus== variables values are rows of tables (t-uples).

For example,

#### Example 1: Find all games

>[!aside | right +++++]
>*Variable* $T$ such that $T$ is in games
$$
\{ T \space | \space T \in \text{games} \}
$$
$$
\{ T \space | \space \exists G \space (G \in \text{games} \land G = T)\}
$$
```sql
SELECT *
FROM games g;
```

#### Example 2: Find the names, versions and prices of the game
>[!note]
>Conjugation is commutative $p \land q \equiv q \land p$

$$
\{ T \space | \space \exists G \space 
	( G \in \text{games} \land 
	\text{T.name} = \text{G.name} \land 
	\text{T.version} = \text{G.version} \land 
	\text{T.price} = \text{G.price})\}
$$

```sql
SELECT g.name, g.version, g.price
FROM games g;
```

#### Example 3: Find the first and last names of the customers in Singapore

$$
\{ T \space | \space \exists C (
	\text{T.firstname} = \text{C.firstname} \land
	\text{T.lastname} = \text{C.lastname} \land
	C \in \text{customers} \land
	\text{C.country} = \text{'Singapore'}
)\}
$$
```sql
SELECT c.firstname, c.lastname
FROM customers c
WHERE c.country = 'Singapore'
```

---

#### Example 4: Find the first and last names of customers and the prices of the games that they have downloaded

{T | ∃C ∃D ∃G (  
T.firstname = C.firstname ∧ T.lastname = C.lastname ∧ T.price = G.price ∧ C∈customers ∧ D∈download ∧ G∈games∧  
D.customerid = C.customerid ∧ D.name = G.name ∧ D.version = G.version)}

```sql
SELECT c.firstname, c.lastname, g.price
FROM customers c, downloads d, games g
WHERE d.customerid = c.customerid
AND d.name = g.name
AND d.version = g.version
```

---

# Relational Algebra
The main algebraic operators are:
- $\cup$ (union)
- $\cap$ (intersection)
- $\setminus$ (non-symmetric difference)
- $\rho$ (renaming)
- $\sigma$ (selection)
- $\pi$ (projection)
- $\times$ (cross)
- $\bowtie$ (inner join)

In *union*, *intersection* and *difference*, the two relation must be ==union-compatible== (ie they must have the same columns)

- Projection (∏) is used to select specific columns (attributes) from a relation while discarding the rest of the columns. It creates a new relation with a subset of the original attributes.

- Selection (σ) is used to select specific rows (tuples) from a relation based on certain conditions (predicates). It filters the tuples that satisfy the specified condition and generates a new relation with only the selected tuples.

In summary, projection focuses on selecting specific columns, while selection focuses on selecting specific rows based on given conditions.