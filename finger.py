from vector import vector
from segment import segment
import math, pygame

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

    def segments(self):
        angle1 = self.perpendicular_angle()
        angle2 = angle1 + math.pi
        ext11 = self.pivot + self.angular_vector(angle1, 8)
        ext12 = self.pivot + self.angular_vector(angle2, 8)
        extreme = self.extreme()
        ext21 = extreme + self.angular_vector(angle1, 5)
        ext22 = extreme + self.angular_vector(angle2, 5)
        return [segment(ext11, ext21, self.color), segment(ext12, ext22, self.color)]
    
    def segment(self):
        return segment(self.pivot, self.extreme(), self.color)

    def extreme(self):
        return self.pivot + self.angular_vector(self.angle, self.length)

    def perpendicular_angle(self):
        return self.angle + math.pi / 2

    def draw(self, screen):
        for segment in self.segments():
            segment.draw(screen)
        pygame.draw.circle(screen, self.color, (self.pivot.x, self.pivot.y), 8)
        pygame.draw.circle(screen, self.color, self.extreme().int().tuple(), 5)


class left_finger(finger):

    def angular_vector(self, angle, length):
        return vector(math.cos(angle), -math.sin(angle)) * length

class right_finger(finger):

    def angular_vector(self, angle, length):
        return (vector(math.cos(angle), -math.sin(angle)) * length).horizontal_mirror()
