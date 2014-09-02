from vector import vector
from segment import segment
from draw import draw_circle
import math


class finger:

    def __init__(self, pivot, length, min_angle, max_angle, color):
        self.pivot = pivot
        self.length = length
        self.min_angle = min_angle
        self.angle = self.min_angle
        self.max_angle = max_angle
        self.color = color
        self.triggered = False

    def update_move(self):
        if self.triggered:
            self.angle += math.pi / 100
            if self.angle > self.max_angle:
                self.angle = self.max_angle
        else:
            self.angle -= math.pi / 200
            if self.angle < self.min_angle:
                self.angle = self.min_angle

    def push(self):
        self.triggered = True

    def release(self):
        self.triggered = False

    def upper_segment(self):
        angle1 = self.perpendicular_angle()
        pivot_upper = self.pivot + self.angular_vector(angle1, 8)
        extreme_upper = self.extreme() + self.angular_vector(angle1, 5)
        return segment(pivot_upper, extreme_upper, self.color)

    def lower_segment(self):
        angle2 = self.perpendicular_angle() + math.pi
        pivot_lower = self.pivot + self.angular_vector(angle2, 8)
        extreme_lower = self.extreme() + self.angular_vector(angle2, 5)
        return segment(pivot_lower, extreme_lower, self.color)

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


class left_finger(finger):

    def angular_vector(self, angle, length):
        return vector(math.cos(angle), -math.sin(angle)) * length


class right_finger(finger):

    def angular_vector(self, angle, length):
        angular_vector = vector(math.cos(angle), -math.sin(angle)) * length
        return angular_vector.horizontal_mirror()
