#notes #cs2102 

>[!quote] In theory….
>The relational model proposes to organise data in [[Introduction & Relational Model#**Relation** | relations]]. Mathematically, relations are subsets of the Cartesian product of the domains of their attributes.

>[!note] In practice
>The RDMS organise data in *tables*, which has a name. Tables are a *multi-sets* of **rows** and **records**. Records have *fields* corresponding to the columns of the table. Columns or fields also have an *implicit position* indicated by the order in the corresponding *creation statement*.

---

# Integrity constraints
>[!note] Definition
>A ==consistent state== of the database is a state which complies with the business rules as defined by the *structural constraints* and the [[Introduction & Relational Model#Integrity constraints | integrity constraints]] in the schema.

If an *integrity constraint* is violated by an operation or a transaction, the operation is **aborted** and **rolled back** and its changes are undone, otherwise, it is committed and its changes are effective for all users.

There are ==five== main kinds of integrity constraints in SQL:
```psql
NOT NULL,
PRIMARY KEY,
UNIQUE,
FOREIGN KEY and
CHECK
```

---

## Primary keys
>[!note] Definition
>A [[Introduction & Relational Model#Key constraints | primary key]] is a ==set== of columns that uniquely identifies a record in the table. Each table has at most one primary key.

>[!aside | right +++++]
>Since it is a set, there cannot be any duplicates.



By its definition, primary key can be one column or a *combination* of columns. An instance of the table cannot have two records with the same value or combination of values in primary key columns and ==primary key column cannot contain a null value==.

Primary key is declared with the keyword `PRIMARY KEY`. In writing the schema, it is underlined.

```sql
CREATE TABLE customers (
	first_name VARCHAR(64),
	last_name VARCHAR(64),
	email VARCHAR(64),
	dob DATE,
	since DATE,
	customerid VARCHAR(16) PRIMARY KEY,
	country VARCHAR(16)
);
```

The primary key constraint prevents any operation or transaction that violates the constraint, for instance, inserting another customer withe the same `customerid`. The operation is aborted and rolled back.

>[!note] Composite primary keys
>Primary keys can be composite and is declared after row declarations.

```sql
CREATE TABLE games (
	name VARCHAR(32),
	version CHAR(3),
	price NUMERIC NOT NULL,
	PRIMARY KEY (name, version)	
);
```

==Not null== constraint guarantees that no value of the corresponding column in any record of the table can be set to null. A not null constraint is always declared as a row constraint. When it is explicit, it is declared with the keyword `NOT NULL`.

Insertion of a `null` value will cause the operation to abort and roll back.

Alternatively, set a default value at table creation time.

## Unique
>[!note] Definition
>A unique constraint on a column or a combination of columns guarantees the table cannot contain 2 records with the same value in the corresponding column or combination of columns.

```sql
CREATE TABLE customers (
    first_name VARCHAR(64) ,
    last_name VARCHAR(64) ,
    email VARCHAR(64) UNIQUE,
    dob DATE,
    since DATE,
    customerid VARCHAR(16) ,
    country VARCHAR(16) ,
    UNIQUE ( first.name , last.name ) ) ;
```

In this example, `customers`‘ `email` must be unique and a ==combination== of `first_name` and `last_name` must be unique **(VERY UNLIKELY)**.

>[!caution] Uniqueness
>This is similar to primary key constraints except that it *does allow `null` values*.

## Foreign key
>[!note] Definition
>A foreign key constraint enforces *referential integrity*. The values in the column for which the constraint is declared must exist in the corresponding columns of the referenced table.

The *referenced columns* are usually required to be the **primary key** of the *referenced table*.

```sql
CREATE TABLE downloads (  
	customerid VARCHAR(16) REFERENCES customers ( customerid ),
	name VARCHAR(32) ,  
	version CHAR(3) ,  
	FOREIGN KEY (name, version) REFERENCES games(name, version)
);
```

A foreign key is declared using `REFERENCES` as a row constraint, and the `FOREIGN KEY` and `REFERENCES` as a table constraint. In the example above, the customer identification number and the combination of name and version of the game she downloaded as recorded in the `downloads` table must correspond to an existing customer and an existing game which must be the corresponding primary keys, `customerid` in the customers table and the combination of `name` and `version` in the `games` table.


## Check
>[!note] Definition
>A `check` constraint enforces any other condition that can be expressed in SQL. A check constraint is declared as a row or a table constraint with the `CHECK` keyword followed by the SQL condition in parenthesis.

```sql
CREATE TABLE games (
	name VARCHAR(32) ,  
	version CHAR(3) ,  
	price NUMERIC NOT NULL CHECK (price > 0)
);
```

In this example, `UPDATE games SET price = price - 10` will result in *negative* prices. This operation is aborted and rolled back.

==Assertion==: Checks outside the table 

---
## Update

>[!caution] What happens when a record in a table is updated or deleted?
>The record may no longer point to a valid key or wrong key from either the table that is referenced or the referencing table.

>[!aside | right +++++]
> >[!quote]
> >Consider all the possible ways to violate the integrity constraints in the code.

The annotations `ON UPDATE` or `ON DELETE` can be initialised to handle delete and update operations.

```sql
CREATE TABLE downloads (  
	customerid VARCHAR(16) REFERENCES customers ( customerid )
		ON UPDATE CASCADE
		ON DELETE CASCADE,
	name VARCHAR(32) ,  
	version CHAR(3) ,  
	FOREIGN KEY (name, version) REFERENCES games(name, version)
		ON UPDATE CASCADE
		ON DELETE CASCADE
);
```

`ON UPDATE CASCADE` — If a record with the `customerid` is deleted, delete the record with `customerid` in `customers`

They are powerful mechanisms that can result in chain reactions when they are chains of foreign key dependencies.


## View

```sql
CREATE VIEW singapore_customers AS
SELECT ...
FROM ...
WHERE country='Singapore'
```

Views create a virtual table instead of *creating* a table of Singapore customers.
Note that a virtual table is better than creating the table as it is updated automatically. However, when a table is created, we need to define triggers and constraints.

## Deferred constraint
>[!note] Definition of *deferred*
>Deferred constraints are not checked until transaction commit

---

# Simple queries

## `SELECT`

```sql
SELECT first_name, last_name
FROM customers
WHERE country = 'Singapore';
```

`SELECT` clause indicates the ==column== to be printed, a `FROM` clause indicates the ==tables== to be queried and *possibly* a `WHERE` clause, which indicates possible condition on the ==records== to be printed.

To select ==ALL== column names, the `*` is a shorthand notation, printing *in order of `CREATE TABLE` declaration*.

```sql
-- SELECT ALL COLUMNS --
SELECT *
FROM customers;

-- SELECT A SUBSET OF THE COLUMNS --
SELECT first_name, last_name
FROM customers;
```

>[!caution]
>Selecting a subset of the columns of a table may result in *duplicate* rows even if the original table has a primary key. This can be made clear with `ORDER BY`.

---

## `ORDER BY`

```sql
SELECT name, version
FROM downloads
ORDER BY name, version;
```

`ORDER_BY` can also be according to column that is not printed, and has optional `ASC/ DESC` to indicate whether the result should be ascending or descending.

>[!note]
>The order of `ORDER BY` implies that it will first order by `name` then if there are ties, it will be broken by `version`.

From a theoretical point of view, a relational database does not have an order as it is a ==set==.

---

## `DISTINCT`

To eliminate duplicates in the result of the query, use `DISTINCT` keyword to return distinct rows, but this does not apply to columns individually. The result is often sorted but cannot rely on this behaviour as this is an unguaranteed side-effect of the sorting algo to eliminate duplicates.

```sql
SELECT DISTINCE name, version
FROM games;
```

>[!caution]
>You can combine different constructs but not always, some combinations does not make sense. For example, both `DISTINCT` and `ORDER BY` involve sorting and conceptually `ORDER BY` is applied before `SELECT DISTINCT`.

Therefore, the following will not work as it will `ORDER BY price` then sort again by `SELECT DISTINCT name`

```sql
SELECT DISTINCT name, version
FROM games
ORDER BY price;
```

>[!caution]
>Think when `DISTINCT` is needed.

---

## `WHERE`

The `WHERE` clause is used to filter rows on ==Boolean== condition. This includes operators such as `AND, OR, NOT`, comparison operators such as `>, <, >=, <=, <>, IN, LIKE, BETWEEN AND`.

```sql
SELECT first_name , last_name  
FROM customers  
WHERE country IN (’Singapore’, ’Indonesia’)  
AND (dob BETWEEN ’2000-01-01’ AND ’2000-12-01’ OR since >= ’2016-12-01’) AND last name LIKE ’B%’;
```

>[!caution]
>The `BETWEEN ... AND ...` is *inclusive*.

---

## Arithmetic operators

```sql
SELECT price * 0.08 AS gst
FROM games
ORDER BY price
```

The above example produces rows of GST where `line 1` aliases the new column as `gst`

You can put arithmetic operators in the `FROM` clause, `WHERE` clause and `ORDER BY` clause.

>[!caution]
>This is not recommended. Use Boolean logic in the `WHERE` clause and leave `CASE` for special cases.
>```sql
>SELECT name || ' ' || version AS game
>CASE
>WHEN price * 0.07 >= 0.3 THEN price * 1.07
>ELSE price
>END
>FROM games
>```

---

## Null values

Every domain has an additional `null` value. In general, the semantics of null values could be ambiguous as it could be *unknown, does not exist, or unknown or does not exist*.

```plain-text
something = null -> unknown (even if something is null)
something <> null -> unknown
something > null -> unknown
something < null -> unknown
10 + null -> null
0 * null -> null
```

When we query with conditions, we will see that `null` values will not be shown.

Therefore, with `null` values, the logic of SQL is a *three valued* logic with unknown. This also means that we cannot use `=` operator to check for `null` values.

Instead, SQL has Boolean operators to check null values and functions to manipulate null values.

```sql
SELECT col1, col2
FROM example
where col2 IS NULL;

SELECT col1, col2
FROM example
where col2 IS NOT NULL;
```

To replace the `null` values, you can `COALESCE().

```sql
SELECT col1, col2, COALESCE(col2, 0)
FROM example
WHERE col2 IS NULL;
```

---

## `COUNT`

`COUNT(*)` counts `NULL` values.
`COUNT(att)` eliminate null values.

---

# Multiple tables

When we query multiple tables, the result is the *Cartesian product*, containing all the columns and all possible combinations of the rows of the tables.

Instead, to make sense, we should join tables according to their *primary keys* and *foreign keys* to make sense of the data.

This is done by adding the condition that *foreign key* columns are equal to the corresponding *primary key* columns.

```sql
SELECT *
FROM customers c, downloads d, games g
WHERE d.customerid = c.customerid
AND d.name = g.name
AND d.version = g.version;
```

>[!caution]
>It is compulsory in this module to systematically define *table variables* for each table in the `FROM` clause and to use these variables with the dot notation. This can also be done with the `AS` keyword.

The `WHERE` clause usually stitches the tables together.

---

# Algebraic queries

## Join

```sql
SELECT *
FROM customers c INNER JOIN downloads d ON d.customerid = c.customerid INNER JOIN games g ON d.name = g.name AND d.version = g.version
```

While this is a cross product between 2 tables, there is no performance difference.

`JOIN` is a synonym of `INNER JOIN`. It is not recommended to use either of them.

`NATURAL JOIN` joins the rows that have the same name to columns and the same values for their columns. It also prints one of the two equated columns.

`OUTER JOIN` keeps the column of the rows in the ==left== (`LEFT OUTER JOIN`, ==right== (`RIGHT OUTER JOIN`) or in ==both== (`FULL OUTER JOIN`) tables that do not match anything in the other table according to the join condition and pad the remaining columns with null values.

>[!caution]
>Note where the table should be. `LEFT` or `RIGHT`?
>
>Be careful where the condition is placed. Otherwise, all records that does not meet the `JOIN` condition will be populated with `NULL`.

```sql
SELECT c.customerid, c.email, d.customerid, d.name, d.version
FROM customers c LEFT OUTER JOIN downloads d ON c.customerid = d.customerid;
```

In the example above, the customers *from the table on the left of the join* who never downloaded a game are combined with `null` values to replace the missing values for the columns of the `download` table. Columns from the *table on the right* of the join are padded with `null` values.

![[leftjoin.png| -m | -center]]

---
```sql
SELECT *
FROM downloads d RIGHT OUTER JOIN games g ON g.name = d.name AND g.version = d.version;
```

In the example above, the games *from the table on the right of the join* that have not been downloaded before are combined with null value to replace the missing values for the columns of the `downloads` table. Columns from the *table on the left* of the join are padded with `null` values.

---

# Set operators

The set operators `UNION, INTERSECT and EXCEPT` return the *union, intersection and non-symmetric difference* of the results of two queries respectively.

>[!caution]
>The two queries must be union-compatible. They must return the same number of columns with the *same domain* in the *same order*.

The operators *eliminate duplicates* unless `ALL` keyword is specified.

### Union operator

```sql
SELECT d.customerid
FROM downloads d
WHERE d.name = 'A' AND d.version = '1.0'
UNION
SELECT d.customerid
FROM downloads d
WHERE d.name = 'A' AND d.version = '2.0'
```

Note that this operation can be done with `OR` operator. However, this will result in duplicates if a customer has downloaded both versions.

### Intersection
```sql
SELECT d.customerid
FROM downloads d
WHERE d.name = 'A' AND d.version = '1.0'
INTERSECT
SELECT d.customerid
FROM downloads d
WHERE d.name = 'A' AND d.version = '2.0'
```
Similarly, this can also be done with `AND` operator. But note that this requires the use of the same table multiple times.

### Except

Except and outer join is expressively similar.

---

# Aggregate queries

The values of a column can be aggregated with ==aggregation functions== such as `COUNT, SUM, MAX, MIN, AVG`

To select the distinct entries in the column of the table, we need to add a `DISTINCT` keyword.

```sql
SELECT COUNT(DISTINCT c.country)
FROM customers c
```

`GROUP BY` clause creates a groups of records that have the same values for the specified fields before computing the aggregate functions.

```sql
SELECT c.country, COUNT(*)
FROM customers c
GROUP BY c.country
```

Groups are formed *after* the rows have been filtered by the `WHERE` clause.

>[!note]
>If we wish to print the columns, they have to be included in the `GROUP BY` clause.
>
>It is recommended and required to include the attributes projected in the `SELECT` clause in the `GROUP BY` clause.

## Using aggregate functions in conditions
>[!caution]
>Aggregate functions are *not allowed* in the `WHERE` clause.

This is because aggregate functions can only be formed after the groups are formed. The groups are formed after rows are filtered by the `WHERE` clause.

Therefore, we need to use `HAVING` clause where `HAVING` clause can only involve aggregate functions on columns listed in the `GROUP BY` clause and subqueries.

```sql
SELECT c.country
FROM customers c
GROUP BY c.country
HAVING COUNT(*) >= 100;
```

---

# Nested queries

Example of nested query where a *subquery* is used in the `FROM` clause

```sql
SELECT d.name
FROM downloads d
WHERE d.customerid IN (
	SELECT c.customerid
	FROM customers c
	WHERE c.country = 'Singapore'
);
```

```sql
SELECT d.name
FROM downloads d
WHERE d.customerid = ANY (
	SELECT c.customerid
	FROM customers c
	WHERE c.country = 'Singapore'
);
```

>[!caution]
>Never use a comparison to a subquery without specifying the qualifier `ALL` or `ANY`.

The query below finds the names and versions of the price of the most expensive games.

```sql
SELECT g1.name, g1.verison, g1.price
FROM games g1
WHERE g1.price >= ALL (
	SELECT g2.price
	FROM games g2
);
```

`ALL` adds expressive power similar to that of `OUTER JOIN, EXCEPT` and aggregate functions.

>[!note] Examples
>Find the countries with largest number of customers:
>```sql
>SELECT c1.country
>FROM customers c1
>GROUP BY c1.country
>HAVING COUNT(*) ≥ ALL (
>	SELECT COUNT(*)
>	FROM customers c2
>	GROUP BY c2.country);
>```

#### Common mistakes

>[!bug] The following do not work:
>```sql
> SELECT g.name, g.version, g.price
> FROM games g
> HAVING g.price = MAX(g.price)
> 
> SELECT g.name, g.version, g.price
> FROM games g
> WHERE g.price = MAX(SELECT g2.price FROM games g2)
> ```

Instead:

```sql
SELECT g.name, g.version, g.price
FROM games g1
WHERE g.price = ALL (
	SELECT MAX(g2.price)
	FROM games g2
);
```

---
### `EXISTS`

>[!note]
>`EXISTS` evaluates to `true` if the subquery has some results and `false` if the subquery has no results.

The subquery is *correlated* to the query

```sql
SELECT d.name
FROM downloads d
WHERE EXISTS (
	SELECT c.customerid
	FROM customers c
	WHERE d.customerid = c.customerid
	AND c.country = 'Singapore'
);
```

In the above example, `d` of the outer query must appear in the `WHERE` clause of the inner query.

>[!bug]
>You can use a column from an outer table in an inner query but not the other way around.

#### Using negation
In this example, we find customers who have never downloaded a game,

```sql
SELECT c.customerid
FROM customers c
WHERE c.customerid NOT IN (
	SELECT d.customerid
	FROM downloads d
)

-- is equivalent to --

SELECT c.customerid
FROM customers c
WHERE NOT EXISTS (
	SELECT d.customerid
	FROM downloads d
	WHERE d.customerid = c.customerid
)
```
