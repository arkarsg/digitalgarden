# Graph
Many data makes more sense if you arrange it as a graph. You can extract more information.

- What does a *node* represent?
- What does an *edge* represent?
	- Can be undirected or directed

In this course, we focus on ==Large Graph Processing==
- Apache Giraph – built just to do graph processing
- Spark

==Graph database==
- A combination of graph processing and graph database
- `neo4j`
- Syntax is similar to SQL

---

# PageRank
>> A simplified version of PageRank

>[!note] Web as a directed graph
>**Nodes** : webpages
>**Edges** : hyperlinks

## Ranking pages
All web pages are not equally **important**. How to measure the *importance* of pages for search recommendation?

>[!example]
>`wikipedia` is being referenced by a lot of other websites (other websites have hyperlinks to `wikipedia`)
>
>Websites such as `nus.edu.sg` will have less hyperlinks directed to it.
>
>$A → B$ implies that there exists a hyperlink in $A$ that directs to $B$

### Links as votes

If many other webpages have a hyperlink directed to a webpage, the webpage will have more votes.

This assumes that incoming links are harder to manipulate. However, users can create a huge number of *dummy* web pages to link to their page to amass votes and drive up its ranks.

**Solution**
Make the number of votes that a page has proportional to its own importance. The dummy pages will have low importance and contribute little votes.

 