package main

import (
	"github.com/blackjack/webcam"
	"fmt"
	"os"
)

func main() {
	 cam, err := webcam.Open("/dev/video0")
	 if err != nil {
	 	panic(err.Error())
	 }

	 defer cam.Close()
	 err = cam.StartStreaming()
	 if err != nil {
	 	panic(err.Error())
	 }

	 for {
	 	err = cam.WaitForFrame(1)

	 	switch err.(type){
		case nil:
		case *webcam.Timeout:
			fmt.Print(os.Stderr, err.Error())
			continue
		default:
			panic(err.Error())
		}

		frame, err := cam.ReadFrame()
		if len(frame) != 0 {
			fmt.Print("We got frame")
		} else if err != nil {
			panic(err.Error())
		}
	 }

}
