# Data Science
Data science is:
- interdisciplinary
- extracting knowledge or insights
- a *continuation* of stats, ML, data mining and predictive analysis

**How to support large-scale data mining with scalable systems and infrastructure?**
- High dimensional data
- Data as a graph
- Infinite data

**Different models of computation**
- MapReduce/ Spark
- Streams and online algorithms
- Large graph processing engines

**How the domain impacts the design of systems and infrastructure?**

## Challenges of big data

### Volume
Refers scale *(size)* of data

Challenges of large volume
- Performance
- Cost
- Reliability
- Algorithm design complexity

![machines_vs_capacity|500](Screenshot%202024-01-21%20at%208.06.27%20PM.png)
>[!caution]
>The sizes here refers to the capacity of the main memory

### Velocity
Refers to the speed of *new* data that is streaming

Challenges of high velocity
- Performance
- Cost
- Reliability
- Algorithm design complexity

### Variety
Refers to the structure and format of the data
- “One size does not fit all”
- Data integration
- Multi-modal learning – data in different format

### Veracity
Refers to accuracy of the data — data quality
- Dirty and noisy data
- Data provenance
- Data uncertainty

In data science operations, *cleansing* takes up the most amount of time

---

# Data lifecycle
An **iterative** process
![data-lifecycle|500](Screenshot%202024-01-21%20at%208.43.41%20PM.png)

>[!info] How to destroy the data?

## Data lake
Sometimes, we do not know if a data is needed or not. So, we just collect them anyways. Storage is cheap and data collected is dumped into a *data lake*

**Data discovery** : the task of finding relevant datasets for analysis
>[!example]
>A global investment bank with more than 100k datasets. How to find risk exposure?

**Data versioning**: Maintain all versions of dataset for storage cost-saving, collaboration, auditing, and experimental reproducibility
>[!example]
>A data science research institution with 1000 - 10k datasets, where datasets are stored in ==HDFS== file system. There are many duplicates being copied for new project, being altered, derived into new ones

![data-lake|500](Screenshot%202024-01-28%20at%201.59.49%20PM.png)

## Common tasks in data lakes
1. Metadata management
2. Ingestion
3. Extraction
4. Cleaning
5. Integration
6. Discovery
7. Versioning

![common-tasks-in-data-lake|500](Screenshot%202024-01-21%20at%208.54.43%20PM.png)

---

# Utility computing
Also known as *Cloud computing*
- Computing resources as a metered service (pay-as-you-go)
- Ability to dynamically provision virtual machines

## Benefits
1. Cost: capital vs operating expenses
	- There is no longer a need to buy high-cost servers
2. Scalability : *infinite* capacity
3. Elasticity : scale up or down on demand

>[!question] Why does it make sense for cloud providers (AWS and GCP)?
>**Economies of scale** : Providers incur a fixed cost, increasing scale → cost per machine becomes smaller