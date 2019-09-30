package main

import (
    "fmt"
    "io/ioutil"
    "log"
    "net/http"
)

func handler(w http.ResponseWriter, r *http.Request) {
    name := makeRequest("http://name_service:8080")
    age := makeRequest("http://age_service:8080")
    fmt.Fprintf(w, "%s is %s years", name, age)
}

func main() {
    http.HandleFunc("/", handler)
    log.Fatal(http.ListenAndServe(":8080", nil))
}

func makeRequest(url string) string {
	resp, err := http.Get(url)
	if err != nil {
		log.Fatalln(err)
	}

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		log.Fatalln(err)
	}

	return string(body)
}