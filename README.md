LEDCube Simulator
=================

This is a simulator I made for creating and testing programs for my LEDCube project.

![Screenshot](http://polyfloyd.net/data/file/2fXWXtC11jvuYbexDjmXTg/LEDCube%20Sim%20Screenshot.png)


## Building

Make sure you have [Go](http://golang.org/dl), GLFW3 and GLEW installed.
On Debian (and maybe Ubuntu) systems, you can install all dependencies with this command:

	sudo apt-get install git golang libgflw3-dev libglew-dev

Finally, install and build ledcubesim:

	git clone https://github.com/PolyFloyd/ledcubesim.git ledcubesim
	cd ledcubesim
	GOPATH=$PWD/gopath go get; go build


## Usage
* Moving the mouse while holding the left mousebutton will cause the view to rotate.
* Scrolling with the mouse adjust the zoom.
* Pressing R on the keyboard will reset the view to its initial condition.
* Pressing S on the keyboard will toggle the visibility of black (off) voxels.


## Command Arguments

	-cx=16: The width of the cube
	-cy=16: The length of the cube
	-cz=16: The height of the cube
	-l=":54746": The TCP host and port for incoming connections


## Network Protocol
The network protocol consists of 3 character commands:

#### frm
Sending `frm` will prepare the program to accept one frame.
To finish, the client must send exactly one frame.
The size of a frame in bytes is determined with `width * height * length * 3`.
Color information is encoded as `RGB`.

#### swp
Sending `swp` swaps the displaybuffers.

#### nfo
Sending `nfo` will cause the program to reply some vendor information.


## Programs
Programs are included in the [programs](programs) directory.
You need Python3 to run these.