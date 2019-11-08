package main

import(
	"regexp"
	"testing"
)

func TestNameCasing(t *testing.T) {
	name := GetName()
	match, _ := regexp.MatchString("^[A-Z]{1}[a-z]+$", name)

	if(match) {
		t.Logf("GetName() PASSED, got %v", name)
	} else {
		t.Errorf("GetName() FAILED, got %v", name)
	}
}