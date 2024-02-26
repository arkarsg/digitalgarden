package main

// Creating rendezvous point with channel -- where goroutines must meet
func main() {
	ch := make(chan int)
	go a(ch)
	go b(ch)
	select {}
}

func a(ch chan int) {
	println("a before")
	ch <- 5 // send the value `5` to the channel
	println("a after")
}

func b(ch chan int) {
	println("b before")
	println(<-ch) // receive a value from channel and print
	println("b after")
}
