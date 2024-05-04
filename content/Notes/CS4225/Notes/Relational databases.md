- Table is in HDFS as a file
# Projection in MapReduce
**Map** : take in a tuple (with tupleID as key) and emit new tuples with appropriate attributes
- No reducer needed → No shuffle step
```sql
SELECT col1, col2 FROM table;
```
# Selection in MapReduce
- Take in a tuple with tuple ID as key
- Emit only tuples that meet the predicate
- No reducer needed
```sql
SELECT *
FROM table
WHERE col > 10;
```
# Aggregation
```sql
SELECT product_id, AVG(price)
FROM sales
GROUP BY product_id
```

In MapReduce:
- Map over tuples, emit `<product_id, price>`
- Framework automatically groups values by keys
- Compute average in **reducer**
- Optimise with combiners

# Relational joins
- Join implementations are complex
- There are different types of `join`

```plain text
If one of the input table is *small*:
	- Broadcast join
Else:
	- Reduce-side join
```

**small** : Can fit into the main memory in a single machine

## Broadcast join
- Requires one of the tables to fit in *main mem* of individual servers
	- All mappers store a copy of the small table (*broadcast*)
	- Spawn mapper based on the big table
	- Iterate over the larger table and join the records with the small table

![](Screenshot%202024-04-16%20at%2011.53.43%20PM.png)
>[!example]
>Consider 2 tables
>- $S$ with 2 tuples
>- $R$ with 6 tuples
>
>Suppose there are $3$ map workers
>1. Copy $S$ to every worker
>2. Perform join for each chunk of $R$ (ie 2 tuples of $R$ per worker)
>3. Emit the result of the join $<key, [R_1, S_1]>$

>[!caution] Why one of the table must fit into main memory?
>If the table cannot fit into memory, it will cause a lot of disk I/O
>
## Reduce-side join
- Doesnt require a dataset to fit in memory, but slower than *broadcast* join
	- Different mappers operate on each table, and emit records, with key as the variable to join by

>[!example]
>Consider 2 tables
>- $S$ with 2 tuples
>- $R$ with 6 tuples
>
>Suppose there are 4 map workers
>1. Each worker reads a chunk from $S$ or $R$
>2. The output of the map worker is $<key, [tuple]>$
>3. Shuffle according to the $key$
>4. Each reduce worker will have records from either $S$ or $R$ with the same $key$
>5. Join locally in the reducer

Works for all cases but it is more costly — need to shuffle both $R$ and $S$, can become a performance bottle neck