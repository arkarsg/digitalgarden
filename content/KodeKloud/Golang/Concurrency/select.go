package main

func main() {
	ch1, ch2 := make(chan int), make(chan int)
	go a(ch2)

	select {
	case value := <-ch1:
		println("1:", value)
	case value := <-ch2:
		println("2:", value)
	}
}
func a(ch chan int) {
	ch <- 5
}
