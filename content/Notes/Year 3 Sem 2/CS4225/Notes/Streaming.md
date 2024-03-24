- In many settings, the data is **arriving over time**; it is not received all at once
	- Streaming approaches are designed to process their input *as it is received*!

![stream-vs-batch](Screenshot%202024-03-24%20at%2010.48.14%20AM.png)

## Streaming Data
- Input elements enter at a rapid rate from **input ports**

1. Elements of the stream are sometimes referred to as *tuples*
2. The stream is potentially infinite
	1. The system cannot store the entire stream accessibly (due to limited memory)

### Example applications
- Data with high volume and constantly arriving over time
	- Sensor data in medical, manufacturing
	- Online customer data
	- Financial transactions, stock trades data

>[!note]
>How to process them in the most efficient way?

---

## Stateful Stream Processing
- Not just perform trivial *record-at-a-time* transformations
- Ability to store and access *intermediate data*
	- How many transactions are already processed
	- State allows recovery
	- Each record will only be executed once
- State can be stored and accessed in many different places
	- Program variables
	- Local files
	- Embedded or external databases

### Spark

#### Micro-batch streaming processing
>[!note]
>Spark does very well on batch processing in a distributed way

- Process streaming data as a list of micro-batches

#### Advantages
- Quickly and efficiently recover from failures
- Deterministic nature ensures end-to-end and exactly-once processing guarantees

#### Disadvantages
- Latencies of a few seconds (cannot achieve $ms$ latencies)

---

## Structured Streaming


---
## Stateful streaming aggregations
- Aggregations not based on time
	- Global aggregation
	- Grouped aggregation

---

## Time semantics
- Processing time : the time of stream processing machine
- Event time : the time an event actually happened

**Event time**
- Decouples processing speed from results
- Operations are predictable and their results are deterministic

---

# Flink
- Native stream processing

## Event-driven streaming application