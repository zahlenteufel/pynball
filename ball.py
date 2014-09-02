import pygame
from vector import vector, distance

ballimg = pygame.image.load('ball.png')

class ball:

	MIDDLE = 0
	BORDER = 1

	GRAVITY_ACC = 0.01

	def __init__(self, center, radius, velocity):
		self.center = center
		self.radius = radius
		self.velocity = velocity

	def intersection(self, segment):
		closest_point = segment.closest_point(self.center)
		if distance(closest_point, self.center) <= self.radius:
			return closest_point
		else:
			return None
		# plength = segment.project_length(self.center)
		# if plength <= 0:
		# 	return self.BORDER, segment.p1
		# elif plength >

		# if p is not None:
		# 	return self.MIDDLE, distance(p, self.center) <= self.radius
		# else:
		# 	if distance(segment.p1, self.center) <= self.radius:
		# 		return self.BORDER, segment.p1
		# 	if distance(segment.p2, self.center) <= self.radius:
		# 		return self.BORDER, segment.p2

	def draw(self, screen):
		screen.blit(ballimg, (self.center.x - self.radius, self.center.y - self.radius))

	def apply_gravity(self):
		self.velocity += vector(0, self.GRAVITY_ACC)

	def apply_colissions(self, segments):
		self.center += self.velocity
		for segment in segments:
			collision_point = self.intersection(segment)
			if collision_point:
				self.center -= self.velocity # undo move
				if segment.is_extreme(collision_point):
					self.velocity = segment.ddir.reflect(self.velocity)
				else:
					orthogonal = (collision_point - self.center).normalized()
					orthogonal.x, orthogonal.y = -orthogonal.y, orthogonal.x
					self.velocity = orthogonal.reflect(self.velocity)
				self.velocity = self.velocity * 0.7