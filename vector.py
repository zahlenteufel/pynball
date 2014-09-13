import math


def distance(v1, v2):
    return (v1 - v2).length()


class Vector:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        else:
            return Vector(self.x * other, self.y * other)

    def int(self):
        return Vector(int(self.x), int(self.y))

    def tuple(self):
        return self.x, self.y

    def horizontal_mirror(self):
        return Vector(-self.x, self.y)

    def length(self):
        return math.hypot(self.x, self.y)

    def normalized(self):
        l = self.length()
        return Vector(self.x / l, self.y / l)

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def reflect(self, other):
        assert abs(self.length() - 1.) < 0.00001
        dot = self * other
        return self * dot * 2 - other
