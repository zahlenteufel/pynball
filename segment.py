from vector import Vector
from draw import draw_line, draw_arrow


class Segment:

    def __init__(self, p1, p2, color):
        self.p1 = p1
        self.p2 = p2
        self.diff = p2 - p1
        self.length = self.diff.length()
        self.direction = self.diff.normalized()
        self.color = color

    def draw(self, screen):
        draw_line(screen, self.p1, self.p2, self.color)
        draw_arrow(screen, (self.p1 + self.p2) * 0.5, (self.p1 + self.p2) * 0.5 + self.normal() * 10)

    def normal(self):
        return Vector(self.direction.y, -self.direction.x)

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


def segments_from_rectangle(x, y, w, h, color):
    corners = \
        [
            Vector(x, y),
            Vector(x + w, y),
            Vector(x + w, y + h),
            Vector(x, y + h)
        ]
    return [
        Segment(corners[0], corners[1], color),
        Segment(corners[1], corners[2], color),
        Segment(corners[2], corners[3], color),
        Segment(corners[3], corners[0], color)
    ]
