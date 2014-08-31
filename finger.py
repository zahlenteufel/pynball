from vector import vector
from segment import segment
import math

RED = (255, 0, 0)

def vector_angle(angle, length):
	return vector(math.cos(angle), -math.sin(angle)) * length

class finger:

	def __init__(self, pivot, length, min_angle, max_angle):
		self.pivot = pivot
		self.length = length
		self.min_angle = min_angle
		self.angle = self.min_angle
		self.max_angle = max_angle

	# def segment(self):
	# 	return segment(self.pivot, self.pivot + vector_angle(self.angle, self.length), RED)

	def retreat(self):
		# pass
		self.angle -= math.pi / 10 # depends on FPS...
		if self.angle < self.min_angle:
			self.angle = self.min_angle

		# self.angle = min(self.min_angle, self.min_angle - math.pi / 100)

	def trigger(self):
		self.angle = self.max_angle


class left_finger(finger):

	def segment(self):
		return segment(self.pivot, self.pivot + vector_angle(self.angle, self.length), RED)

class right_finger(finger):

	def segment(self): # mirrored
		return segment(self.pivot, self.pivot + vector_angle(self.angle, self.length).horizontal_mirror(), RED)
