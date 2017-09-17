package main

import (
	v "github.com/tomaszheflik/vectors"
	"fmt"
)

func main() {
	pointV10 := v.Point{1, 1}
	pointV11 := v.Point{10, 10}
	vector, err := v.GetVector(pointV10, pointV11)
	if err != nil {
		fmt.Printf("Got error %+v" err)
	}
	fmt.Printf("Vector from points: %+v", vector)
	}