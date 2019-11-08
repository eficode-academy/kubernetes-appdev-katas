package main

import (
    "fmt"
    "log"
	"net/http"
    "math/rand"
    "time"
)

func GetAge(min int, max int)(int) {
    rand.Seed(time.Now().UnixNano())
	return rand.Intn(max - min) + min
}

func handler(w http.ResponseWriter, r *http.Request) {
    min := 0
    max := 100
    
	fmt.Fprintf(w, "%d", GetAge(min, max))
}

func main() {
    http.HandleFunc("/", handler)
    log.Fatal(http.ListenAndServe(":8080", nil))
}
