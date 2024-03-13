
# Data types

- String : sequence of chars
- Number
    - Integer (4 bytes or 8 bytes)
    - Float
- Boolean
- Arrays & Slices
    - Contains single datatype
    - Slices : Flexible array like d-type, more control over mem allocation
- Maps
    - Collection of key-value pairs

## Typing
Types are either explicitly declared by a programmer or is inferred by the compiler

**Result** : Fast, statically typed, compiled language that feels like a dynamically typed, interpreted language.

```go
package main

import "fmt"

func main() {
    name := "Golang beginner" // implicity assings `name` as string
    fmt.Println(name)
}
```

---

# Numbers

## Integers `int`
- `int` : Signed integers
- `uint` : Unsigned integers

## Float
- `float32` : single precision
- `float64` : double precision

## String `string`
- Occupies 16 bytes of mem

## Boolean `bool`
- `true` and `false`
- Go does not allow `0` and `1` for truth values
- Occupies 1 byte of mem

---

# Named variables

Initialising a variable

```go
var <variable name> <data type> = <value>
```

```go
var s string = "Hello world"
var i int = 100
```

```go
package main
import ("fmt")

func main() {
	var greeting string = "Hello world"
	fmt.Println(greeting)
}
```

## Shorthands
```go
package main
import ("fmt")

func main() {
	var s, t string = "foo", "foo2"
	fmt.Println(s, t)
}
```

**Short variable declaration**

```go
package main
import ("fmt")

func main() {
	s := "Hello world"
	fmt.Println(s)
}
```

**Not allowed**

```go
package main
import ("fmt")

func main() {
	s := "Hello world"
	s = 12
	fmt.Println(s)
}
```

---

# Zero values

When a variable is initialised but not assigned, there is a default value. These are known as `zero values`


| D type                               | Zero value |
| ------------------------------------ | ---------- |
| Bool                                 | `false`    |
| Int                                  | `0`        |
| Float                                | `0.00`     |
| String                               | `“”`       |
| pointers, functions, interfaces, map | `nil`      |


