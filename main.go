/*
 * Copyright (c) 2014 PolyFloyd
 */

package main

import (
	"flag"
	"io"
	"os"
)

const (
	INFO                 = "PolyFloyd's LEDCube Simulator v0.1"
	UI_DRAGDIV   float32 = 240.0
	UI_FOVY      float32 = 45.0
	UI_SPACING   float32 = 8.0
	UI_WIN_H     int     = 768
	UI_WIN_W     int     = 1280
	UI_ZFAR      float32 = 2048.0
	UI_ZNEAR     float32 = 1.0
	UI_ZOOMACCEL float32 = 12.0
)

func main() {
	cx := flag.Int("cx", 16, "The width of the cube")
	cy := flag.Int("cy", 16, "The length of the cube")
	cz := flag.Int("cz", 16, "The height of the cube")
	c := flag.Int("c", 0, "Set all dimensions to the same size")
	flag.Parse()

	x, y, z := *cx, *cy, *cz
	if *c != 0 {
		x, y, z = *c, *c, *c
	}
	disp := NewDisplay(x, y, z)

	go func() {
		buf := make([]byte, disp.NumVoxels()*3)
		for {
			_, err := io.ReadFull(os.Stdin, buf)
			if err != nil {
				break
			}
			fbuf := make([]float32, disp.NumVoxels()*3)
			for i, c := range buf {
				fbuf[i] = float32(c) / 255.
			}
			disp.Show(fbuf)
		}
	}()

	disp.Run()
}
