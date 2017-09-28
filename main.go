package bikefit

import (
	v "github.com/tomaszheflik/vectors"
	"fmt"
)

func main() {
	start1 := v.Point{10, 10}
	stop1 := v.Point{30, 10}
	vector1, err1 := v.GetVector(start1, stop1)

	start2 := v.Point{10, 10}
	stop2 := v.Point{40, 30}
	vector2, err2 := v.GetVector(start2, stop2)

	if err1 != nil || err2 != nil {
		fmt.Printf("Got error %+v, %+v", err1, err2)
	}

	ang1,ang2 := v.GetAngel(vector1, vector2)
	fmt.Printf("RAD: %+v, DEG: %+v\n", ang1, v.Round(ang2, 0.05))
}