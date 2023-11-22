```sql
SELECT COUNT(*)
FROM loan l, student s1, student s2
WHERE (
    l.borrower = s1.email AND
    l.owner = s2.email AND
    s1.department = s2.department
)

SELECT DISTINCT d.faculty, COUNT(*)
FROM department d, loan l, student s1, student s2
WHERE (
    l.borrower = s1.email AND
    l.owner = s2.email AND
    s1.department = s2.department
)
GROUP BY d.faculty;

```

```sql
# a

# b
SELECT s.name
FROM student s
WHERE s.email
IN (
	SELECT c.owner
	FROM copy c
	WHERE NOT EXISTS (
		SELECT *
		FROM loan l
		WHERE c.copy = l.copy AND
			c.book = l.book AND
			c.owner = l.owner
	)
)

# c
SELECT d.department, s.name, COUNT(*) 
FROM student s, loan l
WHERE l.owner = s.email
GROUP BY s.department, s.email
HAVING COUNT(*) >= ALL(
	SELECT COUNT(*)
	FROM student s1, loan l1
	WHERE
		l1.owner = s1.email AND
		s.department = s1.department
	GROUP BY s1.email
);

SELECT s.email, s.name
FROM student s
WHERE NOT EXISTS (
	SELECT *
	FROM book b
	WHERE authors = 'Adam Smith'
		AND NOT EXISTS (
			SELECT *
			FROM loan l
			WHERE l.book = b.isbn13
			AND l.borrower = s.email
		)
)
```

