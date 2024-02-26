package main

// `go` keyword start several concurrent executing functions
func main() {
	go a()
	go b()
	select {} // prevents function from termination
}

func a() {
	go aa()
	go ab()
}

func aa() { println("aa") }

func ab() { println("ab") }

func b() {
	go ba()
	go bb()
}

func ba() { println("ba") }
func bb() { println("bb") }
