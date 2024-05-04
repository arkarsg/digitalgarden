- **Mixing host language with SQL**
	- Write a language that mixes a host language with SQL
	- Pass it to a preprocessor which returns a program in the host language
	- Compile the program to executable code

---
# SQL Functions
- Each of the following *returns some values / tuples*

---

## Returning a datatype

Suppose we want to convert number grade to letter grade as follows:

```sql
CREATE OR REPLACE FUNCTION convert(mark INT)
RETURNS char(1) AS
$$
	SELECT CASE
		WHEN mark >= 70 THEN 'A'
		WHEN mark >= 60 THEN 'B'
		WHEN mark >= 50 THEN 'C'
		ELSE 'D'
		END;
$$
LANGUAGE sql;
```

---
## Returning a tuple

Returning an existing *tuple*

```sql
CREATE OR REPLACE FUNCTION topStudent()
RETURNS Scores AS
$$
	SELECT *
	FROM Scores
	ORDER BY Mark DESC
	LIMIT 1;
$$
LANGUAGE sql;
```

---
## Returning a set of tuples

Returning an existing *set* of tuples

```sql
CREATE OR REPLACE FUNCTION topStudents()
RETURNS SETOF Scores AS
$$
	SELECT *
	FROM Scores
	WHERE Mark = (
		SELECT MAX(Mark)
		FROM Scores)
	);
$$
LANGUAGE sql;
```
>[!note]
> Here, we are returning a **SETOF**


---
## Returning a new tuple

- In the above two examples, we are returning tuples/ set of tuples in the **Scores** table
- How to return some other tuple?

---
Create a function that returns the highest mark and its number of occurrences

```sql
CREATE OR REPLACE FUNCTION topMarkCnt(OUT TopMark INT, OUT Cnt INT)
RETURNS RECORD AS
$$
	SELECT Mark, COUNT(*)
	FROM Scores
	WHERE Mark = (
		SELECT MAX(Mark)
		FROM Scores
	)
	GROUP BY Mark;
$$
LANGUAGE sql;
```

>[!note] 
>Here, we are returning a **RECORD**

---

## Returning a new *set* of tuples

Create a function that returns each distinct mark and its number of occurrences

```sql
CREATE OR REPLACE FUNCTION MarkCnt(OUT Mark INT, OUT Cnt INT)
RETURNS SETOF RECORD AS
$$
	SELECT Mark, COUNT(*)
	FROM Scores
	GROUP BY Mark;
$$
LANGUAGE sql;
```

## Returning a table
```sql
CREATE OR REPLACE FUNCTION MarkCnt()
RETURNS TABLE(Mark INT, Cnt INT) AS
$$
	SELECT Mark, COUNT(*)
	FROM Scores
	GROUP BY Mark;
$$
LANGUAGE sql;
```

---

# Procedures
If no return value / tuple is needed, we may use SQL procedures instead.

```sql
CREATE OR REPLACE PROCEDURE transfer(fromAcct TEXT,
									 toAcct TEXT,
									 amount INT)
AS
$$
	UPDATE Accounts
	SET balance = balance - amount
	WHERE name = fromAcct

	UPDATE Accounts
	SET balance = balance + amount
	WHERE name = toAcct
$$
LANGUAGE sql
```

>[!note]
>- We are creating a ==procedure==.
>- There are no return values

Call the procedure with
`CALL transfer('Alice', 'Bob', 100);`

---

# Control structure
- `IF ... THEN ... ELSE ... ENDIF`
- `LOOP ... END LOOP`
- `WHILE ... LOOP ... END LOOP`
- `FOR ... IN ... LOOP ... ENDLOOP`

## Variables
- Declare the variables at the start of the program
```sql
CREATE OR REPLACE FUNCTION swap(INOUT val1 INT, INOUT val2 INT)
RETURNS RECORD AS
$$
	DECLARE
		temp_val INTEGER;
	BEGIN
		temp_val := val1;
		val_1 := val2;
		val_2 := temp_val;
	END;
$$
LANGUAGE plpgsql;
```

```
SELECT swap(11, 22) // returns (22, 11)
```

---

# Cursors

Suppose we have a sorted records of students based on their marks. For each student, we want to compute the difference between their mark with the previous student.

1. Sort the students with `ORDER BY ... DESC`
2. Loop over the sorted sequence of students
	1. Here, we need to use a ==Cursor==

>[!note]
>A cursor enables us to access each individual row returned by a `SELECT` statement

![[Screenshot 2023-11-26 at 12.21.57 PM.png|500]]

```sql
CREATE OR REPLACE FUNCTION score_gap()
RETURNS TABLE(name TEXT, mark INT, gap INT)
AS
$$
	DECLARE
		-- declare cursor variable --
		curs CURSOR FOR (
			SELECT *
			FROM Scores
			ORDER BY Mark DESC
		);
		r RECORD;
		prv_mark INT;

	BEGIN
		prv_mark := -1;
		-- Executes the SQL statement and points the cursor to the start--
		OPEN curs;

		LOOP
			FETCH curs INTO r; -- Read the next tuple from curs into r
			EXIT WHEN NOT FOUND; -- terminate if there are no records

			name := r.Name;
			mark := r.Mark;
			IF prv_mark >= 0 THEN gap := prv_mark - mark;
			ELSE gap := NULL;
			END IF;

			RETURN NEXT; -- inserts a tuple to the output of the func
			prv_mark := r.Mark;
		END LOOP;
		CLOSE curs; -- release all resources allocated to curs
	END;
$$
LANGUAGE plpgsql;
```

---

Write a function that retrieves the student(s) with the *median* marks

1. Sort the students by descending order of marks
2. If $n$, the number of students, is odd
	1. Median = $(n + 1) / 2$-th student
- If $n$ is even
	- Median = $(n / 2)$ and $(n / 2) + 1$-th students

```sql
CREATE OR REPLACE FUNCTION median_stu()
RETURNS SETOF Scores AS
$$
DECLARE
	curs CURSOR FOR (SELECT * FROM Scores ORDER BY Mark DESC);
	r RECORD;
	n INT;

BEGIN
	OPEN curs; -- execute the SQL statement and point to the first rec
	SELECT COUNT(*) INTO n FROM Scores; -- number of students

	IF n % 2 = 1 THEN
		FETCH ABSOLUTE (n + 1) / 2 FROM curs INTO r;
		RETURN NEXT r;
	ELSE
		FETCH ABSOLUTE (n / 2) FROM curs INTO r;
		RETURN NEXT r;
		FETCH ABSOLUTE (n / 2) + 1 FROM curs INTO r;
		RETURN NEXT r;
	ENDIF;
	CLOSE curs;
END;
$$
LANGUAGE plpgsql
```

>[!caution]
>When we are returning a *SETOF* records instead of a *TABLE*, we immediately return the record $r$. Note that in *TABLE*, we need to assign `name` and `mark` from the record $r$.