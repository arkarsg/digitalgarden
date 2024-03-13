/**
Array is a numbered sequence of elements of a specific length

- Slices are more common
*/

package main
import "fmt"

func main() {
	var a [5]int					// create an array that can hold 5 ints -- default: zero-valued

	a[4] = 100						// Set the 4-th index to 100
	fmt.Println("Set", a)
	fmt.Println("get", a[4])
	fmt.Println("Length", len(a))	// Get the length of array

	b := [5]int{1, 2, 3, 4, 5}		// Declare and initialise an array
	fmt.Println(b)

	var mat [3][3]int				// Multi-dimensional data structure

	for i := 0; i < 3; i++ {
		for j:=0; j < 3; j++ {
			mat[i][j] = i + j
		}
	}

	fmt.Println("3x3 Matrix: ", mat)
}
