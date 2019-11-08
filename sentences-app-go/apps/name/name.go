package main

import (
    "fmt"
    "log"
	"net/http"
	"math/rand"
	"time"
)

func GetName() (string) {
	names := [5]string{"Graham", "John", "Terry", "Eric", "Michael"}

	rand.Seed(time.Now().UnixNano())
	return names[rand.Intn(len(names))]
}

func handler(w http.ResponseWriter, r *http.Request) {
	name := GetName()

	fmt.Fprintf(w, "%s", name)
}

func main() {
    http.HandleFunc("/", handler)
    log.Fatal(http.ListenAndServe(":8080", nil))
}
