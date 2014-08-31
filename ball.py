import pygame
from vector import vector

def dist(p1, p2):
	return (p1 - p2).length()

ballimg = pygame.image.load('ball.png')

class ball:

	MIDDLE = 0
	BORDER = 1

	GRAVITY_ACC = 0.2

	def __init__(self, center, radius, velocity):
		self.center = center
		self.radius = radius
		self.velocity = velocity

	def intersection(self, segment):
		p = segment.project(self.center)
		if p is not None:
			return self.MIDDLE, dist(p, self.center) <= self.radius
		else:
			if dist(segment.p1, self.center) <= self.radius:
				return self.BORDER, segment.p1
			if dist(segment.p2, self.center) <= self.radius:
				return self.BORDER, segment.p2

	def draw(self, screen):
		screen.blit(ballimg, (self.center.x - self.radius, self.center.y - self.radius))

	def apply_gravity(self):
		self.velocity += vector(0, self.GRAVITY_ACC)

	def apply_colissions(self, segments):
		self.center += self.velocity
		for segment in segments:
			collision = self.intersection(segment)
			if collision is not None and collision[1]:
				self.center -= self.velocity # undo move
				if collision[0] == self.MIDDLE:
					self.velocity = segment.ddir.reflect(self.velocity)
				else:
					p = collision[1]
					ort = (p - self.center).normalized()
					ort.x, ort.y = -ort.y, ort.x
					self.velocity = ort.reflect(self.velocity)
				self.velocity = self.velocity * 0.7