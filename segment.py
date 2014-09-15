import pygame
from vector import Vector


class Segment:

    def __init__(self, p1, p2, color):
        self.p1 = p1
        self.p2 = p2
        self.diff = p2 - p1
        self.length = self.diff.length()
        self.direction = self.diff.normalized()
        self.color = color

    def draw(self, screen):
        pygame.draw.line(
            screen,
            self.color,
            self.p1.tuple(),
            self.p2.tuple(), 1)

    def normal(self):
        return Vector(-self.direction.y, self.direction.x)

    def closest_point(self, point):
        plength = self.projected_length(point)
        if plength <= 0:
            return self.p1
        elif plength >= self.length:
            return self.p2
        else:
            return self.p1 + self.direction * plength

    def is_extreme(self, point):
        return point == self.p1 or point == self.p2

    def projected_length(self, point):
        return (point - self.p1) * self.direction

    def project(self, point):
        plength = self.projected_length(point)
        if 0 <= plength <= self.length:
            return self.p1 + self.direction * plength
        else:
            return None
