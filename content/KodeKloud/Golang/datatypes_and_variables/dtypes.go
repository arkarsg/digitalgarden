package main
import (
	"fmt"
	"reflect" // reflect the type
	"strconv" // string conversion
)

func main() {
	printDtypes()
	typeCast()
	toString()
}

func printDtypes() {
	var grade int = 42
	var message string = "Hello word"
	hintedString := "type hinted as string"
	hintedFloat := 99.9

	fmt.Printf("grade is of type %T and has value of %v\n", grade, grade)
	fmt.Printf("message is of type %T and has value of %v\n", message, message)
	fmt.Printf("hintedString is of type %T and has value of %v\n", hintedString, hintedString)
	fmt.Printf("hintedFloat is of type %T and has value of %v\n", hintedFloat, hintedFloat)
	fmt.Printf("grade is of type %v\n", reflect.TypeOf(grade))
}

func typeCast() {
	var intValue int = 90
	var floatValue float64 = float64(intValue)
	println(floatValue)
}

func toString() {
	var value int = 42
	var s string = strconv.Itoa(value)
	fmt.Println(s, reflect.TypeOf(s))

	var s2 string = "42"
	value2, err := strconv.Atoi(s2)
	fmt.Println(value2, err, reflect.TypeOf(value2))
}
