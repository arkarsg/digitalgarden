# Database design process

>[!note]
>There are *2* main activities in the database design process:
>
> - Database design
> - Applications design

>[!caution]
>How to design the conceptual schema for a database application?

![[databasedesign.png|80%]]


# Entity relationship diagrams

>[!caution] ER model
>ER model has *3* main concepts:
>
> 1. Entities (and their entity types and entity sets)
> 2. Attributes (simple, composite, multivalued)
> 3. Relationships (and their relationship types and relationship sets)

![[ernotation.png|80%]]

---

## Company database example

To illustrate, use a ==COMPANY== database:
>> The company is organised into ==departments==. Each department has a name, number and an ==employee== who *manages* the department. We keep track of the *start date* of the department manager. A department may have several *locations*.
>> 
>> Each department *controls* a number of ==PROJECTS==. Each project has a *unique name*, *unique number* and is located at a *single location*.

- Each employee works for *one department* but may work on *several projects*
- The DB will keep track of the *number of hours per week* that an employee currently works on each project
- It is required to keep track of the ==DIRECT SUPERVISOR== of each employee
- Each employee may have a number of ==DEPENDENTs==
	- For each dependent, the DB keeps a record of name, sex, birthdate, and relationship to the employee.

![[entityexamples.png|50%]]

---

## Entities and attributes

>[!note] Entity
>Entity is a basic concept of the ER model. Entities are specific things or objects that are represented in the database.

>[!note] Attributes
>Attributes are properties used to describe an entity.

A ==specific entity== will have a value for each of its *attributes*. Each *attribute* has a value set (or data type) associated with it.

### Types of attributes
**Simple** : Each entity has a single *atomic* value for the attribute.

**Composite** : The attribute may be composed of several components.
		- For example, `Name(firstName, middleName, lastName)`
		- Composition may for a hierarchy where some components are themselves composite 

**Multi-valued** : An entity may have multiple values for that attribute. This may also be nested arbitrarily to any number of levels

![[compositeattribute.png|80%]]

### Entity types

Entities with the same basic attributes are grouped or typed into an entity type.

An *attribute* of an entity type for which each entity have a *unique value* is called ==key attribute== of the entity type.

The key attributes may be *composite* or an entity type may have *more than one key*.

Each key is <u>underlined.</u>

>[!caution]
>Note that this is different from the relational schema where only one *primary key* is underlined.



![[entityset.png|80%]]

### Entity set
>[!note] Entity set
>Entity set is the current *state* of the entities of that type that are stored in the database.

### Domains of attributes
Each ==simple== attribute is associated with a value set. A ==value set== specifies the set of values associated with an attribute.

In SQL, this is captured in terms of data type.

We refer to the value of attribute $A$ for entity $e$ as $A(e)$.
Value sets are similar to data types in most programming languages.

---

>[!summary] In ER diagrams
> ==An entity type== is displayed in a rectangular box.
> 
> ==Attributes== are displayed in ovals connected to its entity type, key attribute underlined and components of a composite attribute are connected to the oval representing the composite attribute.
> 
> ==Multivalued attributes== displayed in *double ovals*

---

## Relationships

A ==relationship== relates two or more distinct *entities* with a specific meaning. Relationships of the same type are grouped or typed into ==relationship type==.

>[!caution] Degree of relationship
>The ==degree== of a relationship type is the number of ==participating entity types==.


```start-multi-column
ID: ID_spc3
Number of Columns: 2
Largest Column: standard
Shadow: off
Border: off
```
### Relationship type
- *Schema description* of a relationship that identifies the relationship name and the participating entity types
- Identify certain relationship constraints
- **Represented** by diamond-shaped box connecting the participating entity types via straight line
- Note that there should not be an arrow
--- column-end ---

### Relationship set
- Current *set* of relationship instances represented in the database
- The current *state* of a relationship type

--- end-multi-column

#### Example
```plain-text
1. Employee -- works for -- Department
2. Employee -- works on -- Project
3. Employee -- manages -- Deparment
```
In the first relationship, observe that it is a *many-to-one* relationship (*N:1*), since there are multiple employees in one department.

In the second relationship, observe that it is a *many-to-many* relationship (*M:N*), since there multiple employees can work on zero or more projects.

---

### Constraints on relationships

>[!note] Constraints on relationship types
>Constraints on relationship types is also known as ==ratio constraints== or ==cardinality ratio constraint== (maximum participation)
>	- One-to-one
>	- One-to-many or many-to-one
>	- Many-to-many
>
> ==Existence dependency== constraint specifies *minimum participation*
> 	- zero (optional participation, not existence-dependent)
> 	- one or more (mandatory participation, existence dependent)

A ==recursive relationship type== is a relationship type between the same *participating entity* type in distinct roles. This is also called a *self-referencing* relationship type.

For example, we have one ==employee== in the *supervisor* role and one ==employee== in the supervisee role.
- Both participations are the same entity type in different roles
- For example, **SUPERVISION** relationships between EMPLOYEE and another EMPLOYEE
- To distinguish the participation, there needs to be ==role names==

### Weak entity types
>[!note] Weak entity types
>Weak entity is an entity that does not have a **key attribute** and that is *identification dependent* on another entity type.

Therefore, they do not have any primary key and cannot be identified on their own, so they depend on some other entity.

It must participate in an *identifying relationship type* with an ==owner== or the ==identifying entity type==.

Weak entity depends on *strong entity* to ensure the existence of weak entity.

Entities are identified by the combination of:
- A partial key of the weak entity type
- The particular entity they are related to in the identifying relationship type

For example, a ==DEPENDENT== entity is identified by the dependent’s first name (*partial key*) and the specific ==EMPLOYEE== whom the dependent is related (*identifying entity type*)

The relationship between a strong and weak entity is represented by ==double diamond==.

---

## Dependencies among entity types


```start-multi-column
ID: ID_zxki
Number of Columns: 2
Largest Column: standard
Shadow: off
Border: off
```

### Existence dependency

Also known as the *minimum participation constraint* between two entity types if an entity cannot exist in the database unless its dependency is present.

--- column-end ---

### Identification dependency

This implies ==weak entity type== and identification dependency implies existence dependency as a natural phenomenon.

--- end-multi-column

>[!caution]
>Note that existence dependency does not imply weakness of entity type:
>
> ![[weakentity.png]]

---

### Attributes of relationship types
- A relationship type can have attributes, where most relationship attributes are used with $M:N$ relationships

For example, an EMPLOYEE works on a PROJECT for $v$ hours. Note that different employee may work different value of hours on the same project. Hence, `Hours` must be an attribute of relationship types.

>[!note]
>In $1:N$ relationships, they can be transferred to the entity type on the $N$-side of the relationship

---

## Notation for constraints on relationships

It is shown by cardinality ratio, written as `participation constraint : total`

Alternatively, it can be specified with `(min, max)` notation for relationship structural constraints.

This implies that each entity $e$ in $E$ participates in at least $min$ and at most $max$ relationship instances in $R$

![[relationshipnotation.png|80%]]

---

# Relationships of higher degree

>[!caution] n-ary relationship
>In general, an ==n-ary== relationship *is not equivalent* to *n* binary relationships.
>
>Constraints are also harder to specify for higher degree relationships.

In a ternary relationship type, every instance of the ternary relationship must have ==one instance== of each participating relationship type.

If a particular binary relationship can be derived from a higher-degree relationship at all times, then it is redundant.