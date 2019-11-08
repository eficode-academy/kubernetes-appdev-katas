package main

import "testing"

func TestAgeIntegerShouldBeBetween(t *testing.T) {
	min := 0
	max := 100
	result := GetAge(min, max)

	if(result >= min) && (result <= max) {
		t.Logf("GetAge(%d, %d) PASSED, expected %d to be between %d and %d", min, max, result, min, max)
	} else {
		t.Errorf("GetAge(%d, %d) Failed, expected %d to be between %d and %d", min, max, result, min, max)
	}
}