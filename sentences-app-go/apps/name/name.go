package main

import (
    "fmt"
    "log"
	"net/http"
	"math/rand"
	"time"
)

func handler(w http.ResponseWriter, r *http.Request) {
	names := [5]string{"Graham", "John", "Terry", "Eric", "Michael"}

	rand.Seed(time.Now().UnixNano())

	fmt.Fprintf(w, "%s", names[rand.Intn(len(names))])
}

func main() {
    http.HandleFunc("/", handler)
    log.Fatal(http.ListenAndServe(":8080", nil))
}
