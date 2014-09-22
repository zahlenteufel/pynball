from vector import Vector, distance
from draw import draw_circle

GRAVITY_ACC = Vector(0, 0.08)
#Vector(0, 0.002)


class Ball:

    def __init__(self, center, radius, velocity):
        self.center = center
        # rename it to position...
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

    def collides_segment(self, segment):
        return self.intersection(segment) is not None

    def at(self, time):
        newPosition = self.center + \
            GRAVITY_ACC * (time ** 2) + self.velocity * time
        newVelocity = self.velocity + GRAVITY_ACC * time
        return Ball(newPosition, self.radius, newVelocity)

    def apply_colissions_to_segments(self, segments):
        for segment in segments:
            collision_point = self.intersection(segment)
            if collision_point:
                self.center -= self.velocity  # undo move
                if segment.is_extreme(collision_point):
                    self.velocity = segment.direction.reflect(self.velocity)
                else:
                    orthogonal = (collision_point - self.center).normal()
                    self.velocity = orthogonal.reflect(self.velocity)
                self.velocity = self.velocity * 0.7
