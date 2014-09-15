from vector import Vector
from segment import Segment
from draw import draw_circle
import math
import copy


class Finger:

    def __init__(self, pivot, length, min_angle, max_angle, color):
        self.pivot = pivot
        self.length = length
        self.min_angle = min_angle
        self.angle = self.min_angle
        self.max_angle = max_angle
        self.color = color
        self.triggered = False

    def angle_at(self, t):
        if self.triggered:
            angle = self.angle + t * math.pi / 100
            if angle > self.max_angle:
                angle = self.max_angle
        else:
            angle = self.angle - t * math.pi / 200
            if angle < self.min_angle:
                angle = self.min_angle
        return angle

    def at(self, t):
        angle = self.angle_at(t)
        res = copy.copy(self)
        res.angle = angle
        return res

    def impact_on(self, ball):
        newball = copy.copy(ball)
        # mysegm = (self.extreme() - self.pivot)
        # distance_to_pivot = mysegm.projected_length(ball.center)
        # assume touched upper segment
        upseg = self.upper_segment()
        newball.velocity = \
            upseg.direction.reflect(newball.velocity) * 0.8
            #  + \
            # upseg.direction.normal() * distance_to_pivot * 0.01
        return newball

    def push(self):
        self.triggered = True

    def release(self):
        self.triggered = False

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

    def collides(self, ball):
        d1 = (ball.center - self.pivot).length()
        d2 = (ball.center - self.extreme()).length()
        if d1 <= ball.radius + 8:
            return True
        if d2 <= ball.radius + 5:
            return True
        for segment in self.segments():
            if ball.collides_segment(segment):
                return True
        return False

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
        angular_vector = Vector(math.cos(angle), -math.sin(angle)) * length
        return angular_vector.horizontal_mirror()
