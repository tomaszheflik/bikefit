package main

import (
	"fmt"
	log "github.com/sirupsen/logrus"
	"image"
	_ "image/jpeg"
	"os"
	"github.com/golang/geo/s2"
	"github.com/golang/geo/r3"
)

func main() {
	point1 := s2.Point{r3.Vector{10,10,10,}}
	point2 := s2.Point{r3.Vector{10, 20,0}}
	point3 := s2.Point{r3.Vector{20, 20,0}}
	fmt.Printf("Kąt %+v\n", s2.Angle(point1, point2, point3))
	minimum := minRGB{65503, 65503, 65503, 0, 0}
	var punkty []minRGB
	reader, err := os.Open("image1.jpg")
	if err != nil {
		log.Printf("Error opening file %+v", err)
	}
	defer reader.Close()

	m, format, err := image.Decode(reader)
	log.Printf("Format: %s", format)
	if err != nil {
		log.Printf("Error decode image %+v", err)
	}
	bound := m.Bounds()
	fmt.Printf("Image size(X:Y) %d:%d\n", bound.Max.X, bound.Max.Y)
	for y := bound.Min.Y; y < bound.Max.Y; y++ {
		for x := bound.Min.X; x < bound.Max.Y; x++ {
			r, g, b, _ := m.At(x, y).RGBA()
			if r > 65000 && g < 20000 && b < 20000 {
				if r > minimum.r || g < minimum.g || b < minimum.b {
					minimum.r = r
					minimum.g = g
					minimum.b = b
					minimum.x = x
					minimum.y = y
				} else {
					punkty = append(punkty, minimum)
				}
			}
		}

	}
	fmt.Printf("Minimum (Y:X) %d:%d\n", minimum.x, minimum.y)
	 for   i ,_ := range punkty {
		fmt.Printf("%v\n", punkty[i])
	 }

	}
