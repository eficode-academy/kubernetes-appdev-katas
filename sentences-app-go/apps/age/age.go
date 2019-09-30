package main

import (
    "fmt"
    "log"
	"net/http"
	"math/rand"
)

func handler(w http.ResponseWriter, r *http.Request) {
	min := 0
    max := 100
    fmt.Println(rand.Intn(max - min) + min)

	fmt.Fprintf(w, "%d", rand.Intn(max - min) + min)
}

func main() {
    http.HandleFunc("/", handler)
    log.Fatal(http.ListenAndServe(":8080", nil))
}
