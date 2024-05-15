A *monotonic* stack is a stack whose elements are monotonically ==increasing== or ==decreasing==

**Decreasing monotonic stack**
Suppose we want to push a new element. If we need to pop *smaller* elements from the stack, then it is a decreasing monotonic stack from bottom to top.

For a decreasing monotonic stack,
```mermaid
flowchart TD
	a["1 (top)"] --> 2 --> 4 --> b["5 (bottom)"]
```

To push `3`, pop all smaller or equal elements ie `[1, 2]`

```mermaid
flowchart TD
	a["3 (top)"] --> 4 --> b["5 (bottom)"]
```

**Increasing monotonic stack**
Suppose we want to push a new element. If we need to pop *larger* elements from the stack, then it is an increasing monotonic stack

For an increasing monotonic stack,

```mermaid
flowchart TD
	a["8 (top)"] --> 5 --> 3 --> b["1 (bottom)"]
```

To push `4`, pop all larger or equal elements ie `[8, 5]`
```mermaid
flowchart TD
	a["4 (top)"]  --> 3 --> b["1 (bottom)"]
```