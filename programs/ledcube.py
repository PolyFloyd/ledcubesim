#
# Copyright (c) 2014 PolyFloyd
#

import os
import socket
import sys

def determineConnection():
	addr = os.getenv("CUBE_ADDR")
	port = os.getenv("CUBE_PORT")

	for (i, arg) in enumerate(sys.argv[1:]):
		if arg == "-a":
			addr = sys.argv[i + 2]
		elif arg == "-p":
			port = int(sys.argv[i + 2])

	if not addr:
		addr = "127.0.0.1"
	if not port:
		port = 54746

	return (addr, port)

class Cube(socket.socket):

	size   = (0, 0, 0)
	colors = 3
	fps    = 0

	def __init__(self, server=determineConnection()):
		super(Cube, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
		self.connect(server)

		self.send(b"inf")
		data = self.recv(4 * 3 + 1 + 1, socket.MSG_WAITALL)
		getInt = lambda offset: int.from_bytes(data[offset:offset + 4], byteorder="little")
		self.size = (
		    getInt(4 * 0),
		    getInt(4 * 1),
		    getInt(4 * 2),
		)
		self.colors = int(data[4 * 3])
		self.fps    = int(data[4 * 3 + 1])

	def swap(self):
		self.send(b"swp")

	def frame(self, data):
		self.send(b"put")
		self.send(data)

	def xyz(self, xyz, rgb=0):
		return (xyz[0]*self.size[0]*self.size[1] + xyz[1]*self.size[1] + xyz[2]) * self.colors + rgb

	def graph(self, func, autoSend=1, autoSwap=1):
		frame = bytearray(self.size[0] * self.size[1] * self.size[2] * 3)
		sx = self.size[0]
		sy = self.size[1]
		sz = self.size[2]
		for x in range(0, sx):
			for y in range(0, sy):
				for z in range(0, sz):
					vox = func(x / sx, y / sy, z / sz)
					for c in range(0, self.colors):
						frame[self.xyz((x, y, z), c)] = int(vox[c] * 255)
		if autoSend:
			self.frame(frame)
			if autoSwap:
				self.swap()

	def length(self):
		return self.size[0] * self.size[1] * self.size[2] * self.colors
