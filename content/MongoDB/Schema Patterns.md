---
title: Schema Patterns
---
# Patterns
Schema patterns are *guidelines* based on the considerations:
1. **Scaling**
2. **Read or write intensive**
3. **Cost**
---
# Representation patterns
These patterns focus on the *representation* of the schema

## Attribute pattern
- Collections that have similar subset of fields
	- Search across many fields
- Some fields are present only in small set of documents

**Aim** : Reduce the number of indexes and make queries faster

Suppose we have `Products` which has *release dates*.

```json
{  
	"name": "Product1",  
	"prize": "90.00",  
	"releasedate_USA": ISODate("2019-05-20T01:00:00+01:00"),  
	"releasedate_Canada": ISODate("2019-05-28T01:00:00+01:00"),  
	"releasedate_China": ISODate("2019-08-20T01:00:00+01:00"),  
	"releasedate_India": ISODate("2019-05-20T01:00:00+01:00"),  
	"releasedate_UK": ISODate("2019-08-20T01:00:00+01:00")  
}
```

- The query will be indexed for *every* `releasedate_*`
- Not every product are released in these countries
- The query and index will not be scalable if a product is released in all the countries

The `releasedate_*` are **similar subset of fields**

```json
{  
	name: "product1",  
	price: "90.00",  
	releases: [  
		{  
			location: "USA",  
			date: ISODate("2019-05-20T01:00:00+01:00")  
		},  
		{  
			location: "Canada",  
			date: ISODate("2019-05-28T01:00:00+01:00")  
		},  
		{  
			location: "China",  
			date: ISODate("2019-08-20T01:00:00+01:00")  
		},  
		{  
			location: "UK",  
			date: ISODate("2019-05-20T01:00:00+01:00")  
		},
		{  
			location: "India",  
			date: ISODate("2019-08-20T01:00:00+01:00")  
		}, 
			…  
		],  
	…  
}
```

Now, when query, it will be indexed in `releases.date`.
- `db.products.find({ releases.date: { $gt: new Date() } )`



