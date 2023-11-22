#cs2102 #notes 

## Overview
- [ ] Why ==database management systems?==
- [ ] ==Challenges== for data-intensive applications
- [ ] From ==file-based== data management to DBMS
- [ ] Core concepts of DBMS (transactions, data abstractions)
- [ ] Relational Database theory
	- [ ] Motivation
	- [ ] Relation, domain, schema
	- [ ] Integrity constraints

--- 

# Common challenges for data-intensive applications

## Efficiency
- There needs to be fast access to information in huge volumes of data

## Transactions
- “All-or-nothing” changes to data

## Data integrity
- Parallel access and changes to data

## Recovery
- Fast and reliable handling of failures from system crashes, power outage, network disruption

## Security
- Fine-grained data access rights

---

# File-based vs Database

==File-based== data management (also known as file system) is a software to organise and access small groups of data. It is responsible for storing and retrieving files from a storage medium.

- [c] High development effort
- [c] Long development times
- [c] Higher risk of **critical** errors – greater change of inconsistency as files can be duplicated etc.

>[! aside | right +++++]
>Requirements such as indexing, caching, security, logging are similar for applications that handle large amount of data. Hence, it can be moved from application logic and grouped into ==DBMS==.

## DBMS

==DBMS== is an application that can manipulate data in more complex and stable way.

The complex, low level code is moved from application logic to DBMS which offers a set of universal and powerful functionalities for data management.

- [p] Faster application development
- [p] Increased productivity
- [p] Higher stability and less errors

---

# Transactions

==Transactions== are a finite sequence of database operations and is the ==smallest logical unit of work== from an application perspective.

## ACID properties of transactions
>[!aside | right +++++ ]
> ==Isolation==  ensures that a transaction seems like the only user of the database.


- **Atomicity**: either all effects of transaction are reflected or none
- **Consistency**: execution of transaction guarantees to yield a correct state of the database
- **Isolation**: execution of transaction is isolated from effects of concurrent transaction
- **Durability**: After commit of transaction, its effects are permanent even in case of failures.

![[assets/dbtransitiongraph.png]]
![](assets/dbtransitiongraph.png){width=300 height=200}

## Concurrent transactions

### **Serializability**

>[!aside | right +++++]
>Two executions are equivalent if they have the same effect on the data

A ==concurrent== execution of a set of transactions is  **serializable** if the execution is equivalent to some ==serial== execution of the same set of transaction.

>[!note] Core tasks of DBMS
>- [i] Support ==concurrent== executions of transactions to optimise performance
>- [i] Enforce serializability of concurrent execution to ensure integrity of data

---

# Architecture of DBMS

![[dbmsarchitecture.png| -center | -m]]

## Data Independence


```start-multi-column
ID: ID_zoi1
Number of Columns: 2
Largest Column: standard
Border: off
Shadow: off
```

#### **Logical data independence**
Ability to change logical schema without affecting external schemas


--- column-end ---

#### **Physical data independence**
- Representation of data independent from physical scheme
- Physical schema can be changed without affecting logical schema


--- end-multi-column

>[!note] Logical vs Physical schema
>**Physical schema**: how the data is stored and its representation, data structure used to achieve the schema of the data base (ie trees, hashing)
>
>**Logical schema**: logical constraints applied in storing the data. Conceptual model of the data

---

# The Relational Model

### **Domain**
>[!aside | right +++++]
>**Atomic value**
>
>A piece of data in a database table that cannot be broken down any further

>[!aside | right +++++]
>$null$ is a special value indicating that $v$ is not known or not specified.


A set of ==atomic== values where $dom(A_{i})$ is the ==domain== of attribute, $A_{i}$.

For each value $v$ of attribute $A_{i}$,
$$v \in dom(A_{i}) \space \textsf{or} \space v = null$$

### **Relation**

> [!aside | right +++++]
> A relation is a **SET**. There should not be any duplicates.


A set of tuples (or records) such that for a schema $R$ with $n$ attributes,

$$R(A_{1}, A_{2}, ..., A_{n})$$

and each ==instance== of $R$ is a relation which is a subset of
$$ \{ (a_{1}, a_{2}, ..., a_{n}) \space | \space a_{i} \in dom(A_{i}) \space \cup \space \{null\} \}$$

### **Relational database schema**
- set of relation schemas + data constraints

### **Relational database**
- collection of tables

---

# Integrity constraints

==Integrity constraint== is a condition that restricts what constitutes a valid data to maintain data integrity.

## 3 main structural integrity constraints
**Structural**: inherent to the data model, independent from the application

  
```start-multi-column  
ID: ExampleRegion4  
number of columns: 3  
border: off  
```

#### Domain constraints
Cannot store `string` in `integer` column

--- end-column ---

#### Key constraints
**Superkey**: ==subset== of attributes that *uniquely* identifies a tuple in a relation.

**Key**: superkey that is also minimal, such that no ==proper== subset of key is a superkey

**Candidate keys**: set of *all* keys for a relation

**Primary key**:  Selected candidate key for a relation where values of primary key attributes cannot be `null`

**Prime attribute**: attribute of *candidate* key

--- end-column ---

#### Foreign key constraints
Subset of attributes of relation `A` if it refers to ==primary== key in a relation `B`

>[!note] Requirement
>Each foreign key in **referencing** relation must:
>
>1. appear as **primary key** in *referenced* relation OR
>2. be a $null$ value

--- end-multi-column

>[!note] Notes on foreign key constraints
> Referencing and referenced relation can be the same relation.
> 
> A relation can be referencing and referenced relation for different relations.

>[!note]
>Structural integrity constraints covers ==application-independent== constraints. 
>
>Integrity constraints are optional.
>
>Integrity constraints may affect performance.

---

# Glossary

|                     |                                                                                                |
| ------------------- | ---------------------------------------------------------------------------------------------- |
| **Data Model**      | ==Set of concepts== for describing the data and ==framework== to specify the structure of a DB |
| **Schema**          | ==Description== of the structure of a DB using the concepts provided by the data model         |
| **Schema instance** | Content of a DB at a particular time                                                           |
| **attribute**       | Column of a table                                                                              |
| **domain**          | Set of possible values for an attribute                                                        |
| **attribute value** | Element of a domain                                                                            |
| **relation schema** | Set of attributes (data types + relation name)                                                 |
| **relation**        | Set of tuples                                                                                  |
| **tuple**           | Row of a table                                                                                 |
| **database schema** | Set of relation schemas                                                                        |
| **database**        | Set of relations/ tables                                                                                               |





