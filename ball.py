from vector import Vector, distance
from draw import draw_circle


class Ball:

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

    def draw(self, screen):
        draw_circle(screen, (255, 255, 255), self.center, self.radius)

    def apply_gravity(self):
        self.velocity += Vector(0, self.GRAVITY_ACC)

    def apply_colissions(self, segments):
        self.center += self.velocity
        for segment in segments:
            collision_point = self.intersection(segment)
            if collision_point:
                self.center -= self.velocity  # undo move
                if segment.is_extreme(collision_point):
                    self.velocity = segment.ddir.reflect(self.velocity)
                else:
                    orthogonal = (collision_point - self.center).normalized()
                    orthogonal.x, orthogonal.y = -orthogonal.y, orthogonal.x
                    self.velocity = orthogonal.reflect(self.velocity)
                self.velocity = self.velocity * 0.7
