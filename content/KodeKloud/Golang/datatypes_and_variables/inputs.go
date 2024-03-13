package main
import "fmt"

func main() {
	// readWithScan()
	// readMultipleVar()
	returnFromScan()
}

func readWithScan() {
	var name string
	fmt.Print("Enter your name: ")
	fmt.Scanf("%s", &name)
	fmt.Println("Hello,", name)
}

func readMultipleVar() {
	var name string
	var is_muggle bool

	fmt.Print("Enter your name and status: ")
	fmt.Scanf("%s %t", &name, &is_muggle)
	fmt.Println(name, is_muggle)
}

func returnFromScan() {
	var a string
	var b int
	fmt.Print("Enter a string and a number: ")
	count, err := fmt.Scanf("%s %d", &a, &b)
	fmt.Println(count, err)
	fmt.Println(a, b)
}
