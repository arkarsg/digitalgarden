# Projection in MapReduce
**Map** : take in a tuple (with tupleID as key) and emit new tuples with appropriate attributes
- No reducer needed → No shuffle step

# Selection in MapReduce
- Emit only tuples that meet the predicate
- No reducer needed

# Aggregation
```sql
SELECT product_id, AVG(price) FROM SALES GROUP BY product_id
```

In MapReduce:
- Map over tuples, emit `product_id, price`
- Framework automatically groups values by keys
- Compute average in reducer
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
	- Iterate over the larger table and join the records with the small table

## Reduce-side join
- Doesnt require a dataset to fit in memory, but slower than *broadcast* join
	- Different mappers operate on each table, and emit records, with key as the variable to join by