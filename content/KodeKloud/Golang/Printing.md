```go
package main
import "fmt"

func main() {
	var name string = "KodeKloud"
	var user string = "examples"
	fmt.Println("Welcom to", name, user)
}
```

# String formatting

```go
package main
import "fmt"

func main() {
	var arg string = "KodeKloud"
	var i int = 78
	fmt.Printf("I am on %v, %f times", arg, i)
}
```


| Format specifier           |        |
| -------------------------- | ------ |
| Value in default format    | `%v`   |
| Formats decimal integer    | `%d`   |
| Type of value              | `%T`   |
| Character                  | `%c`   |
| Quoted characters/ strings | `%q`   |
| Plain string               | `%s`   |
| Boolean true or false      | `%t`   |
| Floating numbers           | `%f`   |
| floating numbers up to 2dp | `%.2f` |

