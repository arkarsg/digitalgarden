---
title: MongoDB Basics
---
# Database

1. Embed data directly
2. Reference another piece of data with `$lookup` operator

## Embedding
- Update related information as a single atomic operation
- Large documents lead to poor query performance

## Referencing
- Reference another document using *unique object id*
- Use `$lookup` operator

---

# Relationships

## One-to-one
- One-to-one data
- Each key contains only one value
- Embedding is preferred

```json
{
    "_id": "ObjectId('AAA')",
    "name": "Joe Karlsson",
    "company": "MongoDB",
    "twitter": "@JoeKarlsson1",
    "twitch": "joe_karlsson",
    "tiktok": "joekarlsson",
    "website": "joekarlsson.com"
}
```

## One-to-few
- A key has a few different values
```json
{
	// other key-value pairs
	"addresses": [
		{ "street": "123 Sesame St", "city": "Anytown", "cc": "USA" },  
        { "street": "123 Avenue Q",  "city": "New York", "cc": "USA" }
	]
}
```

## One-to-many
If there are a lot of related entities, then it is one-to-many.

### Product

```json
{
    "name": "left-handed smoke shifter",
    "manufacturer": "Acme Corp",
    "catalog_number": "1234",
    "parts": ["ObjectID('AAAA')", "ObjectID('BBBB')", "ObjectID('CCCC')"]
}
```

### Part
```json
{
    "_id" : "ObjectID('AAAA')",
    "partno" : "123-aff-456",
    "name" : "#4 grommet",
    "qty": "94",
    "cost": "0.94",
    "price":" 3.99"
}
```

>[!note]
>In referencing, the related entities are stored in separate documents and referenced using identifiers, such as object IDs. In embedding, the related entities are nested within the document itself. 
>
>So, while both referencing and embedding can be used in both one-to-few and one-to-many relationships, the distinction lies in the number of related entities rather than the specific technique used.
---
>[!tip] Embedding
>Embedding is preferred unless there is a compelling reason to do so

>[!tip] Referencing
>Needing to access an object on its own is a compelling reason not to embed it

---

## Arrays
Note that in both *embedding* and *referencing*, we are using **arrays** to form the relationship.

>> What if the relationship grows without bound and as a result, the array grows without bounds?

With *high-cardinality*, create an additional document, similar to *foreign keys*.

### Referenced
```json
{
    "_id": ObjectID("AAAB"),
    "name": "goofy.example.com",
    "ipaddr": "127.66.66.66"
}
```

### Referencing
```json
{
    "time": ISODate("2014-03-28T09:42:41.382Z"),
    "message": "cpu is on fire!",
    "host": ObjectID("AAAB")
}
```

---
## Many-to-many

In many-to-many, the documents involved in the relationship are both referencing and referenced. Can perform [normalization](Normalization.md)

### Users
```json
{
    "_id": ObjectID("AAF1"),
    "name": "Kate Monster",
    "tasks": [ObjectID("ADF9"), ObjectID("AE02"), ObjectID("AE73")]
}
```

### Tasks
```json
{
    "_id": ObjectID("ADF9"),
    "description": "Write blog post about MongoDB schema design",
    "due_date": ISODate("2014-04-01"),
    "owners": [ObjectID("AAF1"), ObjectID("BB3G")]
}
```
>[!caution]
>When we have to update the task array in Users, we have to:
>1. Update the task in `tasks` of `User` document
>2. Update the `owners` of `Tasks` document
>
>In other words, we have to perform *two* updates and no longer possible to use a single atomic update
---

# Summary
Consider a one-to-$N$
- Embed the $N$ side if the cardinality is *one-to-few* and there is **no need** to access the embedded object outside the context of the parent object
- Use an array of $N$ objects if the cardinality is *one-to-many* or if the $N$-side objects should stand alone for any reasons
- Use a reference to the *one* side if $N$ is very large

# References
- [MongoDB best practices](https://www.mongodb.com/developer/products/mongodb/mongodb-schema-design-best-practices/)