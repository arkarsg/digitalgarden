>[!note]
>Trigger is a special type of [[Programming with SQL|function]] in SQL

- Returns a `TRIGGER`
- `NEW` and `OLD` syntax

```sql
CREATE OR REPLACE FUNCTION socres_log_func()
RETURNS TRIGGER AS
$$
BEGIN
	INSERT INTO AUDIT(Name, EntryDate)
	VALUES (new.Name, CURRENT_DATE);
	RETURN NEW;
$$
LANGUAGE plpgsql;
```

---

Suppose we want to insert a tuple into `Scores_Log` to record:
- the `name` of the student and
- the `date` of insertion,
Whenever a new tuple is inserted into `Scores`

- If there is an *insertion* into *Scores*
	- Insert into *Scores_Log*

Then, we need
- **Triggers** : Check the condition *insertion* whenever appropriate
- **Trigger function** : Express the condition about an insertion occurring on Scores

# Trigger

```sql
CREATE TRIGGER scores_log_trigger
AFTER INSERT ON Scores
FOR EACH ROW EXECUTE FUNCTION scores_log_func();
```

- Essentially a *listener* for insertion on *Scores*
- Calls the trigger function *after* each insertion of a tuple

# Trigger function

```sql
CREATE OR REPLACE FUNCTION scores_log_func() RETURNS TRIGGER
AS
$$
BEGIN
	INSERT INTO scores_log(Name, EntryDate)
		VALUES(NEW.name, CURRENT_DATE);
	RETURN NULL;
END;
$$
LANGUAGE plpgsql;
```

- `NEW` refers to the new row inserted into *Scores*
- Only `TRIGGER` has access to `NEW`

---

## Access
Trigger functions can also access
- Operations that activates the trigger : *insertion, update, delete*
- Name of table that caused the trigger invocation
- `OLD` : the old tuple being *updated* or *deleted*

---

# Return values
The *return value* depends on the ==trigger timing==

- `AFTER` indicates the trigger function is executed *after* insertion
- `BEFORE` : before insertion
- `INSTEAD OF` : execute the trigger function instead of the trigger operation

## Before
![[Screenshot 2023-11-26 at 1.00.19 PM.png|500]]

## After
![[Screenshot 2023-11-26 at 1.00.58 PM.png|500]]

---

# Trigger levels

In the example so far, we are using *row-level* trigger that executes the trigger function for every tuple encountered.

```sql
CREATE TRIGGER ...
AFTER ...
FOR EACH STATEMENT EXECUTE FUNCTION ...
```

---

# Trigger condition
Use `WHEN` in the *trigger* so that if only calls the trigger function if it meets the condition.

>[!caution]
>- No `SELECT` in `WHEN`
>- No `OLD` in `WHEN` for `INSERT`
>- No `NEW` in `WHEN` for `DELETE`
>- No `WHEN` for `INSTEAD OF`

---
# Deferred trigger
If we have a *constraint* on trigger, declare as *deferrable* and *initially deferred* to defer the constraint check.

```sql
CREATE CONSTRAINT TRIGGER bal_check_trigger
AFTER INSERT OR UPDATE OR DELETE ON account
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW
EXECUTE FUNCTION bal_check_func();
```

With the above trigger, 
```
BEGIN TRANSACTION;
UPDATE Account SET Bal = Bal - 100 WHERE AID = 1;
UPDATE Account SET Bal = Bal + 100 WHERE AID = 2;
COMMIT;
```

The trigger is only activated at commit instead of *update* on each row.

