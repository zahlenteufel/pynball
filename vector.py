import math

class vector:

	def __init__(self, x, y):
		self.x = x
		self.y = y

	def __add__(self, other):
		return vector(self.x + other.x, self.y + other.y)

	def __sub__(self, other):
		return vector(self.x - other.x, self.y - other.y)

	def __mul__(self, other):
		if isinstance(other, vector):
			return self.x * other.x + self.y * other.y
		else:
			return vector(self.x * other, self.y * other)

	def int(self):
		return vector(int(self.x), int(self.y))

	def to_tuple(self):
		return self.x, self.y

	def horizontal_mirror(self):
		return vector(-self.x, self.y)

	def length(self):
		return math.hypot(self.x, self.y)

	def normalized(self):
		l = self.length()
		return vector(self.x / l, self.y / l)

	def __str__(self):
		return "(" + str(self.x) + ", " + str(self.y) + ")"

	def reflect(self, other):
		assert abs(self.length() - 1.) < 0.00001
		dot = self * other
		return self * dot * 2 - other