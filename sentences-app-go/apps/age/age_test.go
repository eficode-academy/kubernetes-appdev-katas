package main

import "testing"

func TestAgeIntegerShouldBeBetween(t *testing.T) {
	min := 0
	max := 100
	result := GetAge(min, max)

	if(result >= min) && (result <= max) {
		t.Logf("GetAge(%v, %v) PASSED, expected %d to be between %v and %v", min, max, result, min, max)
	} else {
		t.Errorf("GetAge(%v, %v) Failed, expected %d to be between %v and %v", min, max, result, min, max)
	}
}