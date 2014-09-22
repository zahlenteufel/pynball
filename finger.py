from __future__ import division
from vector import Vector
from segment import Segment
from draw import draw_circle
import math
import copy


def clamp(value, minv, maxv):
    return max(minv, min(maxv, value))


class Finger:

    def __init__(self, pivot, r1, r2, length, min_angle, max_angle, color):
        assert(r1 >= r2)
        self.pivot = pivot
        self.r1 = r1
        self.r2 = r2
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

    def impact_on(self, ball, remaining_time):
        newball = ball.at(0)
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

        # find the factor such that in the next iteraction they wont collide..

        newball.velocity = ref.reflect(newball.velocity) * 0.8

        nextball = newball.at(remaining_time)
        nextfinger = self.at(remaining_time)

        if nextfinger.collides(nextball):
            fL = 0
            fR = 100
            nball = nextball.at(0)
            nball.velocity += normal * fR
            nball = nball.at(remaining_time)
            assert(not nextfinger.collides(nball))
            while fR - fL > 0.001:
                fmid = (fL + fR) / 2
                nball = nextball.at(0)
                nball.velocity += normal * fmid
                nball = nball.at(remaining_time)
                if nextfinger.collides(nball):
                    fL = fmid
                else:
                    fR = fmid
            nextball.velocity += normal * fR
            nextball = nextball.at(remaining_time)

        # assert the ball and the finger are not colliding at +time_remaining

        return nextball

    def push(self):
        self.angular_velocity = math.pi / 75

    def release(self):
        self.angular_velocity = -math.pi / 30

    def segments(self):
        return [self.upper_segment(), self.lower_segment()]

    def extreme(self):
        return self.pivot + self.angular_vector(self.angle, self.length)

    def draw(self, screen):
        for segment in self.segments():
            segment.draw(screen)
        draw_circle(screen, self.color, self.pivot, self.r1)
        draw_circle(screen, self.color, self.extreme(), self.r2)

    def collides_with_pivot(self, ball):
        return (ball.center - self.pivot).length() < ball.radius + self.r1

    def collides_with_extreme(self, ball):
        return (ball.center - self.extreme()).length() < ball.radius + self.r2

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


class LeftFinger(Finger):

    def angular_vector(self, angle, length):
        return Vector(math.cos(angle), -math.sin(angle)) * length

    def upper_segment(self):
        angle = self.angle + math.acos((self.r1 - self.r2) / self.length)
        pivot_upper = self.pivot + self.angular_vector(angle, self.r1)
        extreme_upper = self.extreme() + self.angular_vector(angle, self.r2)
        return Segment(pivot_upper, extreme_upper, self.color)

    def lower_segment(self):
        angle = self.angle - math.acos((self.r1 - self.r2) / self.length)
        pivot_lower = self.pivot + self.angular_vector(angle, self.r1)
        extreme_lower = self.extreme() + self.angular_vector(angle, self.r2)
        return Segment(extreme_lower, pivot_lower, self.color)


class RightFinger(Finger):

    def angular_vector(self, angle, length):
        return Vector(-math.cos(angle), -math.sin(angle)) * length

    def upper_segment(self):
        angle = self.angle + math.acos((self.r1 - self.r2) / self.length)
        pivot_upper = self.pivot + self.angular_vector(angle, self.r1)
        extreme_upper = self.extreme() + self.angular_vector(angle, self.r2)
        return Segment(extreme_upper, pivot_upper, self.color)

    def lower_segment(self):
        angle = self.angle - math.acos((self.r1 - self.r2) / self.length)
        pivot_lower = self.pivot + self.angular_vector(angle, self.r1)
        extreme_lower = self.extreme() + self.angular_vector(angle, self.r2)
        return Segment(pivot_lower, extreme_lower, self.color)
    
