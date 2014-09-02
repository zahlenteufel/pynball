import pygame
from vector import vector

class segment:

	def __init__(self, p1, p2, color):
		self.p1 = p1
		self.p2 = p2
		self.diff = p2 - p1
		self.dlength = self.diff.length()
		self.ddir = self.diff.normalized()
		self.color = color

	def draw(self, screen):
		pygame.draw.line(screen, self.color, (self.p1.x, self.p1.y), (self.p2.x, self.p2.y), 1)

	def normal(self):
		return vector(-self.ddir.y, self.ddir.x)

	def projected_length(self, point):
		return (point - self.p1) * self.ddir

	def project(self, point):
		plength = self.projected_length(point)
		if 0 <= plength <= self.dlength:
			return self.p1 + vector(plength * self.ddir.x, plength * self.ddir.y)
		else:
			return None