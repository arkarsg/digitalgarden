package main

import (
	"fmt"
	"reflect"
)

func main() {
	// initialising a typed const
	const typed string = "Typed Constant"
	const untyped = "Untyped constant"
	fmt.Println(reflect.TypeOf(typed), reflect.TypeOf(untyped))

	// changing the value of const causes a panic
	assignConst()
}

func assignConst(){
	const i = 42
	i = 43
}
