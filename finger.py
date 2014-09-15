from vector import Vector
from segment import Segment
from draw import draw_circle
import math
import copy


def clamp(value, minv, maxv):
    return max(minv, min(maxv, value))


class Finger:

    def __init__(self, pivot, length, min_angle, max_angle, color):
        self.pivot = pivot
        self.length = length
        self.min_angle = min_angle
        self.angle = self.min_angle
        self.max_angle = max_angle
        self.color = color
        self.angular_velocity = 0

    def angle_at(self, t):
        angle = self.angle + self.angular_velocity * t
        return clamp(angle, self.min_angle, self.max_angle)

    def at(self, t):
        angle = self.angle_at(t)
        res = copy.deepcopy(self)
        res.angle = angle
        if res.angle in (self.min_angle, self.max_angle):
            res.angular_velocity = 0
        return res

    def impact_on(self, ball):
        newball = copy.deepcopy(ball)
        mysegm = (self.extreme() - self.pivot)
        distance_to_pivot = mysegm.projected_length(ball.center)
        # assume touched upper segment
        if self.collides_with_upper_segment(ball):
            normal = self.upper_segment().direction.normal()
        elif self.collides_with_lower_segment(ball):
            normal = self.lower_segment().direction.normal()
        elif self.collides_with_extreme(ball):
            normal = (ball.center - self.extreme()).normalized()
        elif self.collides_with_pivot(ball):
            normal = (ball.center - self.pivot).normalized()
        else:
            assert(False)

        ref = normal.normal()

        newball.velocity = \
            ref.reflect(newball.velocity) * 0.8 + \
            normal * self.angular_velocity * distance_to_pivot * 0.8

        # if ball is moving against finger...

        return newball

    def push(self):
        self.angular_velocity = math.pi / 100

    def release(self):
        self.angular_velocity = -math.pi / 200

    def upper_segment(self):
        angle1 = self.perpendicular_angle()
        pivot_upper = self.pivot + self.angular_vector(angle1, 8)
        extreme_upper = self.extreme() + self.angular_vector(angle1, 5)
        return Segment(pivot_upper, extreme_upper, self.color)

    def lower_segment(self):
        angle2 = self.perpendicular_angle() + math.pi
        pivot_lower = self.pivot + self.angular_vector(angle2, 8)
        extreme_lower = self.extreme() + self.angular_vector(angle2, 5)
        return Segment(pivot_lower, extreme_lower, self.color)

    def segments(self):
        return [self.upper_segment(), self.lower_segment()]

    def extreme(self):
        return self.pivot + self.angular_vector(self.angle, self.length)

    def perpendicular_angle(self):
        return self.angle + math.pi / 2

    def draw(self, screen):
        for segment in self.segments():
            segment.draw(screen)
        draw_circle(screen, self.color, self.pivot, 8)
        draw_circle(screen, self.color, self.extreme(), 5)

    def collides_with_pivot(self, ball):
        return (ball.center - self.pivot).length() < ball.radius + 8

    def collides_with_extreme(self, ball):
        return (ball.center - self.extreme()).length() < ball.radius + 8

    def collides_with_lower_segment(self, ball):
        return ball.collides_segment(self.lower_segment())

    def collides_with_upper_segment(self, ball):
        return ball.collides_segment(self.upper_segment())

    def collides(self, ball):
        return \
            self.collides_with_pivot(ball) or \
            self.collides_with_extreme(ball) or \
            self.collides_with_upper_segment(ball) or \
            self.collides_with_lower_segment(ball)

    # def is_ball_inside(self, ball):
    #     upseg = self.upper_segment()
    #     lowseg = self.lower_segment()
    #     sg1 = (ball.center - upseg.p1) * upseg.normal()
    #     sg2 = (ball.center - lowseg.p1) * lowseg.normal()
    #     return sg1 * sg2 < 0


class LeftFinger(Finger):

    def angular_vector(self, angle, length):
        return Vector(math.cos(angle), -math.sin(angle)) * length


class RightFinger(Finger):

    def angular_vector(self, angle, length):
        return Vector(-math.cos(angle), -math.sin(angle)) * length
