#### Question 1

##### NUNStAClean
- Drops the tables if they exist, cleaning script.

##### NUNStASchema
- Defines the tables in the schema and the integrity constraints.

##### NUNStABook
- Populate the book table (no bug)

##### NUNStAStudent
- Populate the student table (no bug)

##### NUNStALoan
- Populate the loan table

##### NUNStACopy
- Populate the copy table
---

#### Question 2

a. Successful addition
b.
```sql
ERROR: Key (isbn10)=(0321197844) already exists.duplicate key value violates unique constraint "book_isbn10_key" ERROR: duplicate key value violates unique constraint "book_isbn10_key" SQL state: 23505 Detail: Key (isbn10)=(0321197844) already exists.
```
c.
```sql
ERROR: Key (isbn13)=(978-0321197849) already exists.duplicate key value violates unique constraint "book_pkey" ERROR: duplicate key value violates unique constraint "book_pkey" SQL state: 23505 Detail: Key (isbn13)=(978-0321197849) already exists.
```

d. OK
e. OK

f. OK
g. OK

h. Delete from LOAN, delete from STUDENT

```sql
DELETE FROM loan
WHERE borrower IN (
    SELECT email
    FROM student
    WHERE department = 'Chemistry'
);

DELETE FROM student s
WHERE s.department = 'Chemistry';
```

---

#### Question 3

>[!note]
>Deferred constraints are not checked until transaction commit.

That means that within a transaction, we can perform any operations to the attribute value. However, at the end of the transaction, it must satisfy the constraint condition.


<center><iframe width="800" height="500" src="https://begriffs.com/posts/2017-08-27-deferrable-sql-constraints.html"></iframe></center>

```sql
BEGIN TRANSACTION;
SET CONSTRAINTS ALL IMMEDIATE;
DELETE FROM book
WHERE ISBN13 = '978 -0321197849 ';

DELETE FROM copy
WHERE book = '978 -0321197849 ';
END TRANSACTION;
```

---

#### Question 4

Not necessary as it has `check` constraint which enforces `> 0` condition. So when a transaction attempts to create a loan record on a copy == 0, it will fail the check constraint and transaction will be rolled back.

Because there is no way to check that a department is correctly under a faculty and that there are many ways to represent a department (FoS, SoC, SOC,)


