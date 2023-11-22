# Informal design guidelines
## Informal guidelines
>[!note] What is relational database design?
>The grouping of attributes to form *good* relation schemas. There are 2 levels of relation schema:
>1. The logical *user view* level
>2. The storage *base relation* level
>   
> Here, we are concerned with the *base relation*

### Criteria for good design
1. **Minimality** : Should express information with minimum number of distinct relations
2. **Lack of redundancy** : Should minimise the amount of redundancy among relations
3. **Information preservation** : Should preserve all information captured by the conceptual design (the requirements and design in the EER must be reflected)
4. **Consistency** : Among the relations
5. **Efficiency** : Typically addressed in the physical design

## Guidelines
#### Each *tuple* in a relation should represent ONE *entity* or relationship instance
- Attributes of different entities should not be mixed in the same relation
- *Only foreign keys* should be used to refer to other entities
- Entity and relationship attributes should be kept apart as much as possible

Otherwise, this is an example of ER schema that is stored redundantly in relations.

When information in ER schema is stored redundantly in relations:
- Wastes storage
- Causes problem with update anomalies

Consider the relational design where *employee* and *project* are in 1 table
>> EMP_PROJ(<u>Emp#, Proj#</u>, Ename, Pname, no_hours)

>[!example]- Update anomaly
>Conceptually it is correct. However, changing the name of project number `P1` from `Billing` to `Customer Accounting` may cause this update to be made for all 100 employees working on project `P1`.

>[!example]- Insertion anomaly
>Cannot insert a project unless an employee is assigned to it. Cannot insert an employee to the table unless they are assigned to a project. Why? Because they are primary keys and cannot be null.

>[!example]- Delete anomaly
>When a project is deleted, it will result in deleting all the employees who work on that project.
>
>Alternately, if an employee is the sole employee on a project, deleting that employee would result in deleting that corresponding project.

![[fd-functional_dependencies.png| -s | -center]]
This shows the functional dependencies where information from 2 or more entity types are mixed. (i.e. there is mixing of entity and relationship information in the relation)

In (a), there are 2 *entities* mixed. In (b), there is a mix of two entity types and a relationship type.

>[!info] Functional dependencies
>Dependencies among attributes

---
#### Design such that it does not suffer from anomalies. If it has to be present, note them so applications can be made to take them into account.

---
#### Relations should be designed such that their tuples will have few `NULL` values as possible

Relations should be designed such that their tuples will have as few NULL values as possible. 

##### Reasons for `NULL`
1. Attribute not applicable or invalid
2. Attribute value unknown
3. Value known to exist but unavailable

- Attributes that are `NULL` frequently could be placed in separate relations (with primary key)
Suppose we have `Person` and `Passport` relation and the design
>> PERSON(<u>SSN</u>, Name, Passport#, Issue_date)

Then, people who do not have a passport will contain `NULL` values in the tuple.

However, when we break the table into `PERSON` and `PASSPORT`,
>> PERSON(<u>SSN</u>, Name)
>> PASSPORT(<u>Passport#</u>, Issue_date, SSN)

The `PASSPORT` table will have fewer entries than `PERSON` and `PERSON` will not have any `NULL` values.

>[!caution]
>Bad designs for a relational database may result in erroneous results in certain `JOIN` operations.
>
>The *lossless join* property is used to generate meaningful results for `join` operations

---

#### Generation of spurious tuples
>[!caution]
>This must be avoided any cost

The ==lossless join== (or *non-additive join property*) is used to guarantee meaningful results for join operations.

>> BUYS(<u>SSN, Item#, Store_name</u>, …)

However, suppose we mapped this data into 2 tables
>> CUST_ITEM(<u>SSN, Item#</u>)
>> CUST_STORE(<u>SSN, Store_name</u>)

This will result in:

```start-multi-column
ID: ID_1mne
Number of Columns: 2
Largest Column: standard
Border: off
Shadow: off
```

| SSN | Item |
| --- | ---- |
| s1  | x1   |
| s1  | x2   |
| s2  | x1   |
| s2  | x2   | 

--- column-end ---

| SSN | Store_name |
| --- | ---------- |
| s1  | t1         |
| s1  | t2         |
| s2  | t2         |
| s2  | t1           |

--- end-multi-column

However, when we `JOIN`, a snippet is created below:

| SSN | Item# | Store_name | JOIN |
| --- | ----- | ---------- | ---- |
| s1  | x1    | t1         |      |
| s1  | x1    | t2         | BAD  |
| s1  | x2    | t1         | BAD  | 
| s1  | x2    | t2         |      |

Note that this results in invalid data that where data is generated as a result of `JOIN`

Therefore, `BUY` relation should not be decomposed into the 2 relations.

The decomposition should result in
1. Non-additive or losslessness of the corresponding joins
2. Preservation of the functional dependencies

*1* is extremely important and cannot be sacrificed

#### Relations should be designed to satisfy the lossless join condition
- No spurious tuples should be generated by doing a natural join of any relations.

---
# Functional dependencies
>[!note] Functional dependencies
>This is a tool for analysing designs

Functional dependencies are used to specify *formal measure* of the goodness of relational designs. *Keys* are used to defined ==normal forms== for relations.

==Functional dependency== : A set of attributes $X$ functionally determines a set of attributes $Y$ if the value of $X$ determines a unique value for $Y$

$X → Y$ holds whenever two tuples have the same value for $X$, they **must** have the same value for $Y$.

FDs are derived from the real-world constraints on the attributes.

>[!example]
> ![[fd-functional_dependencies.png| -s | -center]]
> In (a), given the SSN, we can uniquely determine the name, date, address and Dnumber
> 
> So, $\text{SSN} → \text{ENAME}$,
> $\text{PNAME} → \{\text{PNAME, Location}\}$

FD is a property of the attributes in the schema $R$. The constraint must hold for every relation instance $r(R)$. If $K$ is a key or $R$, then $K$ functionally determines all attributes in $R$.

An FD is a *semantic* property of the attributes in the schema $R$.

We can only conclude given the instance of a relation is that an FD may exist between certain attributes. However, we can conclude that certain FDs do not exist because there are tuples that show a violation of those dependencies.

>[!example] Ruling out FDs
>We can say that *Text → Course* may exist. However, *Teacher → Course*, *Teacher → Text*, *Course → Text* are ruled out.

| Teacher | Courses         | Text     |
| ------- | --------------- | -------- |
| Smith   | Data Structures | Bartram  |
| Smith   | Data Management | Martin   |
| Hall    | Compilers       | Hoffman  |
| Brown   | Data Structures | Horowitz | 

---

## Inference rules for FDs
An FD $X → Y$ is inferred or implied by a set of dependencies $F$ specified on $R$ if $X → Y$ holds in every legal relation state $r$ of $R$. That is, whenever $r$ satisfies all the dependencies in $F$, $X → Y$ also holds in $r$

### Armstrong’s inference rules
- **Reflexive** : If Y is a subset of X then X → Y
- **Augmentation** : If X → Y, then XZ → YZ (X union Z determines Y union Z)
- **Transitive** : If X → Y and Y → Z, then X → Z

**Sound** : Given a set F that holds in R, every dependency that can be inferred using the rules will hold in every state in R
**Complete** : These rules and all other extended rules that hold can be applied to a set F of dependencies in R until no more dependencies can be inferred — cover of the dependencies.

>[!example]- Reflexivity
>- NRIC, name → NRIC
>- StudentID, Name, Age → Name, Age
>- ABCD → ABC
>- ABCD → BCD

>[!example]- Augmentation
>- NRIC → Name, then NRIC, Age → Name, Age
>- NRIC, Salary, Weight → Name, Salary, Weight

>[!example]- Transivity
>If NRIC → Address and Address → Postal code then NRIC → Postal code

---
### Additional inference
These inferences are based on the fundamental inference rules.

**Decomposition** : If X → YZ then X → Y and X → Z
- Note that the right hand side can be broken up but not the left hand side. (ie you cannot decompose AB → C) 

**Union** : If X → Y and X → Z then X → YZ
**Pseudo-transitivity** : If X → Y and WY → Z then WX → Z

---

## Closure
1. Closure of a set $F$ of FDs is the set $F^+$ of all FDs that can be inferred from $F$
2. Closeure of a set of *attributes* $X$ with respect to $F$ is the set $X^+$ of all attributes that are functionally determined by $X$

$X^+$ can be calculated by repeatedly applying inference rules using the FDs in $F$

```
X+ = X
repeat
	oldX+ = X+
	for each functional dependency Y -> Z in F
		if X+ is in Y then X+ = X+ union Z
until X+ = oldX+
```

>[!example]- Example of closure
>Classes held at a university in a given academic year
>> CLASS(sectionid, course#, instr_name, credit_hrs, text, publisher, classroom, capacity)
>
>**Assumption** : The same instructor may offer the same course# in an assigned classroom on different days — these will get different sectionids. Different instructors may choose different texts for the same course
>
>Let $F$ be the set of functional dependencies for the above relation that include the following FDs
>1. sectionid → course#, instr_name, credit_hrs, text, publisher, classroom, capacity
>2. Course# → credit_hrs
>3. {Course#, instr_name} → Text, classroom
>4. Text → Publisher
>5. Classroom → capacity
>
>The closures of attributes or set of attributes for some example sets:
>{ classid }$^+$ = CLASS
>{ Course#, instr_name }$^+$ = { Course#, instr_name, credit_hrs, text, publisher, classroom, capacity }
---
## Equivalence sets of FDs
Two sets of FDs, $F$ and $G$ are equivalent if:
- Every FD in $F$ can be inferred from $G$, and
- Every FD in $G$ can be inferred from $F$
- Hence, $F$ and $G$ are equivalent if $F^+ = G^+$

$F$ **covers** $G$ if every FD in $G$ can be inferred from $F$ (ie $G^+$ is a subset of $F^+$)

$F$ and $G$ are equivalent if $F$ covers $G$ and $G$ covers $F$.

---

## Finding minimal covers of FDs
An attribute in a functional dependency is considered **extraneous** attribute if we can remove it without changing the *closure* of the set of dependencies.

A set of FDs is minimal if it satisfies the following conditions:
1. Every dependency in $F$ has a single attribute for its RHS
2. We cannot remove any dependency from F and have a set of dependencies that is equivalent to F
3. We cannot replace any dependency X → A in F with a dependency Y → A and still have a set of dependencies that is equivalent to F

```
Set F = E
Replace each functional dependency X -> {A1, A2, ... , An} in F by the n functional dependencies X -> A1, X -> A2

For each functional dependency X -> A in F
	For each attribute B that is an element of X
		if { {F - {X -> A} union { (X - {B}) -> A } } is equivalent to F
			then replace X -> A with (X - {B} ) -> A in F

For each remaining functional dependency X -> A in F if {F - {X -> A} }
is equivalent to F, then remove X -> A from F
```

>[!example]
>Suppose we have FD : { B → A, D → A, AB → D }. Find the minimum cover
>
>- All the above dependencies are in canonical form as they only have 1 attribute on the RHS
>- Then we need to determine if AB → D has any redundant attribute on the right
>- Since B → A, augment both sides, BB → AB or B → AB. However, AB → D
>- Now, we have a set { B → A, D → A, B → D }. No further reduction is possible in step 2 since all FDs have a single attribute on the LHS
>- In step 3, we look for a redundant FD in E’. By using the transitive rule on B → D and D → A, we derive B → A. Hence, B → A is redundant in E’ and can be eliminated.
>- Hence the minimum cover of E is { B → D, D → A}

Every set of FDs has an equivalent minimal set.

There can be *several* equivalent minimal sets for a given set F of FDs. There is no simple algorithm for computing a minimal set of FDs that is equivalent to a set F. The process of algorithm is used until no further reduction is possible.

The different minimum covers can be obtained from starting the algorithm at different FDs.

>[!example] Exactly 1 attribute on the LHS
> FD = { ssn → stud_id, email, stu_id → ssn, email_id, email_id → stu_id, ssn }
>1. Transform all the FDs such that RHS has only 1 attribute
>	1. SSN → stud_id
>	2. SSN → email
>	3. stu_id → ssn
>	4. stu_id → email_id
>	5. email_id → stu_id
>	6. email_id → ssn
>2. Now all the FDs only have 1 attribute on the LHS so there is no need to remove redundant attributes on LHS
>3. Cover each FD, and see whether they can be implied by others
>	- Pretend you do not have the FD, such as ssn → stu_id
>	- ssn → email → stu_id $\implies$ ssn → stu_id
>	- Therefore, you can eliminate ssn → stu_id from the set
>	Perform this for all the remaining FDs.
>4. Minimum cover = { SSN → Email, stu_id → email, email → stu_id, email → SSN }

>[!example] More than 1 attributes on LHS
>Suppose after step 1, we have A → C, AC → D, AD → B, CD → E, CD → F, E → F.
>We wish to make the LHS only have 1 attribute.
>
>For example, in AC → D we cover A and find out if C → D. Therefore, A is required in this FD. Now, cover C and find out if A → D. We see that A → C and C → D. Therefore, A → D and C is not needed in AC → D.
>
>We can now continue with step `3` of the previous example.
---
# Keys and attributes
A ==superkey== of a relation schema $R = \{A_1, A_2, … , A_n \}$ is a set of attributes $S$ subset of $R$ with the property that no two tuples $t_1$ and $t_2$ in any legal relation state $r$ of $R$ will have $t_1[S] = t_2[S]$

A ==key==, $K$ is a *superkey* with the additional property that removal of any attribute from $K$ will cause $K$ not to be a superkey anymore.

- Multiple keys in a relational schema → each is a *candidate key*
	- One of them is *arbitrarily* designated to be *primary key*
- A ==prime attributte== must be a member of some candidate key
- A ==non-prime attribute== is not a member of any candidate key



# Normalisation
>[!note]
>How the design can improve or *purify*
>
>Normal form is a condition using keys and FDs of a relation to certify whether a relation schema is in a particular normal form

==Normalisation== is the process of decomposing *bad* relations by breaking up their attributes into smaller relations by the process of *decomposition*

**Result** : Resulting designs are of high quality and meet the desirable properties

>[!caution] Denormalisation
>The process of storing the join of higher normal form relations as a base relation – which is in a lower normal form. Responsible to keep the relations consistent and to handle the anomalies

## Normal form
Condition using keys and FDs of a relation to certify whether a relation schema is in a particular state of *goodness*.

### 1NF
>[!note]
>For the relation to be in 1NF, every attribute must be functionally dependent on the primary key

Does *not* allow
- composite attributes
- multi-valued attributes
- **nested relations** — attributes whose values for an individual tuple are non-atomic

>[!caution] Not a good design
![[normalization-1nf.png| -m | -center]]
> - Unnecessary redundancy thrown in to follow the 1NF.

>[!example] FD analysis
>Suppose we have the relation
>> DEPARTMENT(<u>Dnumber</u>, Dname, Dmgr_ssn, Dlocations)
>
> and the functional dependecy
>> $F_1$ : Dnumber → Dname, Dmgr_ssn
>
>For a relation to be in 1NF, every attribute must be functionally dependent on the primary key
>
>In the relation above Dnumber does not imply Dlocations. Therefore, the relation does not meet the 1NF requirement.
>
>Break into two tables:
>DEPARTMENT1(<u>Dnumber</u>, Dname, Dmgr_ssn)
>DEPARTMENT2(<u>Dnumber</u>, <u>Dlocation</u>)
>
>Department2 has no FDs

#### Normalizing nested relations into 1NF
Break the nested attribute into another table
>[!example]
>EMP_PROJ(<u>Ssn</u>, Ename, Proj(Pno, hours))
>
>The nested relation PROJ behaves like a composite nested attribute with local key being Pno.
>
>Hence, Ssn does not imply PROJ and only FD is Ssn → Ename). There are attributes that are not functionally dependent on the key.
>
>Ssn , Pno → Hours
>Remedy by creating a new relation that accommodates the nested relation with a join primary key
>EMP_PROJ1(<u>Ssn</u>, Ename)
>EMP_PROJ2(<u>Ssn, Pno</u>, Hours)

### 2NF
>[!note]
>A relation is in second normal form if every *non-prime attribute* $A$ in $R$ is fully functionally dependent on the primary key, or *every* key of $R$ (multiple candidate keys)
>>[!info]
>**Prime attribute** : An attribute that is member of the primary key $K$
>**Full functional dependency** : A FD Y → Z where removal of any attribute from Y means the FD does not hold anymore

>[!example]  Full functional dependency
>SSN, PNUMBER → Hours is a full FD since neither SSN → Hours nor Pnumber → Hours hold

#### Functional dependency analysis
Suppose we have
>> EMP_PROJ(<u>Ssn, Pnumber</u>, hours, Ename, Pname, Plocation)

And the following set of FDs
1. Ssn, Pnumber → Hours
2. Ssn → Ename
3. Pnumber → Pname, Plocation

The non-prime attributes are *hours, ename, pname and plocation*. Since ename, pname and plocation are not fully functionally dependent on **Ssn, Pnumber**, $2$ and $3$ are in violation of 2NF.

#### Decomposition
Decompose to *achieve full functional dependency* on primary key in each relation, and **preserve all FDs**.

### 3NF
>[!info] Transitive dependency
>**Transitive functional dependency** : a FD $X → Z$ that can be derived from $X → Y$ and $Y → Z$

>[!note]
>A relation is in 3NF if:
>1. it is in 2NF
>2. No *non-prime* attribute $A$ in $R$ is transitively dependent on the *primary key*
> 
> The general definition: A relation schema $R$ is in **3NF** if whenever $X → A$ holds in $R$ then *at least* one holds:
>1. $X$ is a superkey of $R$ or *(catches 2NF violations)*
>2. $A$ is a prime attribute of $R$ *(catches transitive dependency)*

The transitivity is only a problem if $Y$ is not a candidate key. If $Y$ is a candidate key, it is not a violation of 3NF.

## Successive normalisation
Given a universal relation, decompose into different relations based on the normal forms. Structurally, it is a tree and the set of relations at the leaf nodes will be the schema at the highest NF.

Suppose
>> LOTS(<u>PropertyId</u>, CountyName, LotNo, Area, Price, TaxRate)

1. PropertyId → LOTS *(primary key)*
2. CountyName, LotNo → LOTS *(candidate key)*
3. CountyName → TaxRate
4. Area → Price

### 2NF
$FD_3$ is not fully functionally dependent on (CountyName, LotNo) which is a candidate key $\implies$ violates 2NF

Decompose into two tables
![[Screenshot 2023-11-21 at 12.14.16 PM.png | -m | -center]]

### 3NF
From $FD_1$, PropertyNo → Area → Price. Since *Area* is a non-prime attribute, there is a transitive dependency which violates 3NF

Decompose the table that violates 3NF
![[Screenshot 2023-11-21 at 12.15.57 PM.png | -m | -center]]

---
>[!summary] Informally…
>**1NF** : All attributes depend on the key
>**2NF** : All attributes depend on the *whole* key
>**3NF** : All attributes depend on *nothing but the key*


>[!info] Other normal forms
>4NF : Based on keys, multi-valued dependencies
>
>5NF : Based on keys, join dependencies
>
>These rarely occur as it depends on multi-valued and join dependencies.

## BCNF
>[!note]
>A relation is BCNF whenever $X → A$ holds in $R$, then $X$ is a superkey of $R$

![[Screenshot 2023-11-21 at 12.28.11 PM.png | -center]]

### Decomposition
A relation not in BCNF should be decomposed so as to achieve BCNF
- Have superkey on the LHS

**Decomposition may forgo the preservation of all functional dependencies**
>[!caution]
>Cannot sacrifice the losslessness property after decomposition

### Binary decomposition
Decomposition of $R$ into two relations
- The FD ($R1 \cap R2 → R1 - R2$) is in $F^+$ or
- the FD ($R1 \cap R2 → R2 - R1$) is in $F^+$

---

# Synthesis

>[!question] How to synthesise good relations based on knowledge of dependencies among attributes?

## Bottom-up design

Assumes that all possible functional dependencies are known (called the universal relation)
1. Construct a minimal set of FDs from the universal relation
2. Then, apply the algorithm that construct a target set of 3NF or BCNF relations
3. Additional criteria may be needed to ensure the set of relations in a relational database are satisfactory

>[!info] Goals
>1. Lossless join property (a must) 
>2. Dependency preservation property
>	- Can forgo by sacrificing the dependency preservation but guarantees losslessness 		

>[!caution]
>Note that this is not used practically as $1.$ is not possible realistically

## Determine the key of a relation
Given a set of functional dependencies $F$ on a universal relation$R$, find a key $K$.

```
Set K = R

for each attribute A in K {
	Compute closure(K - A) with respect to F

	if closure(K - A) contains all the attributes in R
		set K = K - {A}
}
```

==Universal relation schema== is a relational schema that includes all the attributes of the database.

>[!example]
>> ORDER (order#, order_date,customer_id, amount, cust_phone#)
> 1. Default key: entire relation
> 2. Start dropping attributes until you find combinations that uniquely determine each row in the table

## Relational decomposition
### Decomposition
is the process of decomposing the universal relation $R$ into a set of relation schemas $D = \{R_1, … , R_n \}$ that will become the relational  database schema by using the functional dependencies.

### Attribute preservation condition
states that each attribute in $R$ will appear in at least one relation schema $R_i$ in the decomposition so that no attributes are lost

An eventual goal of decomposition is to have each individual $R_i$ in the decomposition $D$ to be in BCNF or 3NF.

The decomposition must not result in spurious tuples — violates lossless join property. Hence, the decomposition will fail the NJB test.

### Dependency preservation property
Given a set of dependencies $F$ on $R$, the *projection* of $F$ on $R_i$, denoted by $\pi_{R_i}(F)$ where $R_i$ is a subset of $R$ is the set of dependencies X → Y in $F^+$ such that all attributes in $X \cup Y$ are all contained in $R_i$.

The projection of $F$ on each relation schema $R_i$ in the decomposition $D$ is the set of functional dependencies in $F^+$ such that all their LHS and RHS attributes are in $R_i$

A decomposition $D$ of $R$ is ==dependency-preserving== with respect to $F$ if the union of the projections of $F$ on each $R_i$ in $D$ is equivalent to $F$


>[!note]
>It is always possible to find a dependency-preserving decomposition $D$ with respect to $F$ such that each relation in $R_i$ in $D$ is in 3NF.

### Non-additive join property

A decomposition $D = \{ R_1, R_2 \}$ of $R$ has the lossless join property with respect to a set of functional dependencies $F$ on $R$:
1. if and only if it satisfies the NJB test
2. if for *every* relation state $r$ of $R$ that satisfies $F$, the following holds, where * is the natural join of all the relations in $D$

$$^*\Big(\pi_{R_1}(r), ... , \pi_{R_m}(r)\Big) = r$$

#### Binary decomposition
![[Functional Dependencies#Binary decomposition]]

All decomposition shown for 2nd and 3rd normalization satisfy the NJB property and hence are good.

#### n-ary decomposition

Suppose we have a universal relation $R$, a decomposition $D$ and a set of functional dependencies $F$,

```
Create an initial matrix S with one row i for each relation R_i in D and one column for each attribute A_j in R

Set S[i][j] = b_ij for all matrix entries where b_ij is a distinct symbol associated with indices i, j

For each row i representing relational schema R_i
	for each column representing attribute A_j
		if R_i includes A_j
			set S[i][j] = a_j

while there is a change in S
	for each FD in F
		for all rows in S which have the same symbols in the columns corresponding to attributes in X
			make the symbols in each column that correspond to an attribute in Y be the same in all these rows as follows
				if any rows has an "a" symbol for the column, set the other rows to that of the same symbol in the column
				if no "a" exists for attribute in any of the rows
					Choose any "b" that appear in one of the rows and set the other rows to that same "b" in the column

if a row is made up entirely of "a" symbols, then the decomposition has the lossless join property. Otherwise, it is not
```

>[!example] Fails the test
>R = {Ssn, ename, pnumber, plocation, hours}
>R_1 = {ename, plocation}
>R_2 = {Ssn, Pnumber, hours, pname, plocation}
>
>F = {Ssn → Ename, pnumber → { pname, plocation}, {ssn, pnumber} → hours }
>
>D = {R_1, R_2}

| Ssn      | Ename    | Pnumber  | Pname    | Plocation | Hours    |
| -------- | -------- | -------- | -------- | --------- | -------- |
| $b_{11}$ | $a_2$    | $b_{13}$ | $b_{14}$ | $a_5$     | $b_{16}$ |
| $a_1$    | $b_{22}$ | $a_3$    | $a_4$    | $a_5$     | $a_6$    | 

>[!example] Passes the test
![[functionaldep-NBJ.png | -center]]

### Successive non-additive join decompositions
If 
1. a decomposition $D = \{ R_1, ... , R_n \}$ of $R$ has the lossless join property with respect to a set of functional dependencies $F$ on $R$, and
2. if a decomposition $D’ = \{ Q_1, ... , Q_k \}$ of $R_i$ has the lossless join property with respect to the *projection* of $F$ on $R_i$,
Then,
- Decomposition $D_2$ of $R$ has the non-additive join property with respect to F where $D_2$ is $D$ with $R_i$ replaced by $D’$

## Algorithms for schema design
### 3NF
Suppose we have a universal set of relation $R$, and a set of functional dependencies $F$ on the attributes of $R$
```
Find a min cover G for F

For each LHS X of FD in G (ie X is the key of this relation)
	R_i = {X + A_1 + A_2 + ... + A_k}
	Add R_i to D

If R_i in D contains key of R
	create R_j = attributes that form the key

Eliminate redundant relations from the resulting set of relations D

R_i is a projection of R_j
	R_i is redundant -> remove

```
>[!example]
>Suppose we have the universal relation
>> $U$(Ssn, Pno, Esal, Ephone, Dno, Pname, Plocation)
>
>And the following FDs
>1. Ssn → Esal, Ephone, Dno
>2. Pno → Pname, Plocation
>3. Ssn, Pno → Esal, Ephone, Dno, Pname, Plocation
>
>FD 3 is the *key* of $U$
>
>1. Determine the *min* cover
>2. This produces relations $R_1$ and $R_2$
>	1. $R_1$(Ssn, esal, ephone, Dno)
>	2. $R_2$(Pno, Pname, Plocation)
>3. Generate a relation corresponding to the key of $U$
>	1. $R_3$(Ssn, Pno)

### BCNF
Given a *universal relation* $R$ and a set of functional dependencies $F$ on the attributes of $R$

```
D = R

while relation schema Q in D is not in BCNF {
	choose a relational schema Q in D that is not in BCNF
	find FD X -> Y in Q that violates BCNF
	replace Q in D by 2 relation schemas (Q - Y) and (X union Y)
}
```

>[!example]
>Suppose we have the universal relation
>>CUST_TABLE(<u>custNo, tableNo, date</u>, waiterNo, billAmount)
>
>And the following FDs
>1. custNo, tableNo, date → waiterNo, billAmount
>2. waiterNo → tableNo
>   
>FD 2 violates BCNF $\implies$ $X$ is waiterNo and $Y$ is tableNo
>1. Remove tableNo from FD 1 (*$Q - Y$*)
>2. Create a relation $X \cup Y$
>
>Decomposition loses FD1 but preserves *non-additive decomposition*

---


