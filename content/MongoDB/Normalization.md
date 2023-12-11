---
title: Normalization
---

In **relational databases**, we normalize the schema.
Here, we are normalizing a *field*.

---

Normalize when:
- High ratio of reads to updates (read frequently, but updated rarely)

This usually:
1. Improves query performance — No *application-level join*
2. introduces redundancy
3. Slower write performance
4. Complex update operations for redundant data

>[!caution]
>Just with [many-to-many](Basics.md#Many-to-many) relationships, normalizing loses *atomic and isolated* updates on that field.

---

## Example
Suppose we have `Productss` and `Parts`

```json
{
    "name": "left-handed smoke shifter",
    "manufacturer": "Acme Corp",
    "catalog_number": "1234",
    "parts": ["ObjectID('AAAA')", "ObjectID('BBBB')", "ObjectID('CCCC')"]
}
```

Suppose we frequently perform *read* on the name of the `Parts`. Then, de-normalized form of `Products` will be:

```json
{
	// other key-value pairs
	"parts": [
		{ "id" : ObjectID('AAAA'), "name" : '#4 grommet' },
		{ "id": ObjectID('F17C'), "name" : 'fan blade assembly' },
		{ "id": ObjectID('D2AA'), "name" : 'power switch' }
	]
}
```

---
# References
- [Denormalzation](https://www.mongodb.com/blog/post/6-rules-of-thumb-for-mongodb-schema-design)

