## Simple queries

>[!aside | right +++++]
>Note that distinct is not necessary for `departments` as it has a primary key on name (ie Unique)

>[!aside | right +++++]
>Distinct is necessary for the 2nd SQL statement as it can be the case where the department has no students enrolled.

>[!aside | right +++++]
>Distinct is necessary for the *3rd* statement as it can be the case where a student is both a borrower and owner.

>[!aside | right +++++]
>Can use `copy` tables too


```sql
SELECT d.department
FROM department d;

SELECT DISTINCT department
FROM student s;

SELECT DISTINCT s.email
FROM student s, loan l
WHERE ( 
	(s.email = l.borrower AND l.borrowed < s.year)
	   OR
	(s.email = l.owner AND l.borrowed < s.year)
	);

SELECT l.returned - l.borrowed + 1 AS duration
FROM loan l
WHERE NOT (l.returned ISNULL)
ORDER BY duration DESC, l.book ASC;

SELECT b.title, s1.name, d1.faculty, s2.name, d2.faculty 
FROM loan l, book b, student s1, department d1, student s2, department d2
WHERE
	(b.publisher = 'Wiley' AND l.returned ISNULL) AND
	(l.borrower = s1.email AND s1.department = d1.department) AND
	(l.owner = s2.email AND s2.department = d2.department) AND
	(l.book = b.ISBN13)

SELECT b.title, s1.name, d1.faculty, s2.name, d2.faculty 
FROM loan l
INNER JOIN student s1 ON l.borrower = s1.email
INNER JOIN department d1 ON s1.department = d1.department
INNER JOIN student s2 ON l.owner = s2.email
INNER JOIN department d2 ON s2.department = s2.department
INNER JOIN book b ON b.ISBN13 = l.book
WHERE
	(l.returned ISNULL AND b.publisher = 'Wiley')


```


#### Question 2

Part b

```sql
SELECT s.email
FROM loan l, student s
WHERE s.email = l.borrower
AND l.borrowed = s.year
UNION
SELECT s.email
FROM loan l, student s
WHERE s.email = l.owner
AND l.borrowed = s.year
```

Part c

```sql
SELECT s.email
FROM loan l, student s
WHERE s.email = l.borrower
AND l.borrowed = s.year
INTERSECT
SELECT s.email
FROM loan l, student s
WHERE s.email = l.owner
AND l.borrowed = s.year
```

Part d

```sql
SELECT s.email
FROM loan l, student s
WHERE s.email = l.borrower
AND l.borrowed = s.year
EXCEPT
SELECT s.email
FROM loan l, student s
WHERE s.email = l.owner
AND l.borrowed = s.year
```