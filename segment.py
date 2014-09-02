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
        pygame.draw.line(
            screen,
            self.color,
            self.p1.tuple(),
            self.p2.tuple(), 1)

    def normal(self):
        return vector(-self.ddir.y, self.ddir.x)

    def closest_point(self, point):
        plength = self.projected_length(point)
        if plength <= 0:
            return self.p1
        elif plength >= self.dlength:
            return self.p2
        else:
            return self.p1 + self.ddir * plength

    def is_extreme(self, point):
        return point == self.p1 or point == self.p2

    def projected_length(self, point):
        return (point - self.p1) * self.ddir

    def project(self, point):
        plength = self.projected_length(point)
        if 0 <= plength <= self.dlength:
            return self.p1 + self.ddir * plength
        else:
            return None
