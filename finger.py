from vector import vector
from segment import segment
import math, pygame

def vector_angle(angle, length):
    return vector(math.cos(angle), -math.sin(angle)) * length

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
                self.triggered = False
        else:
            self.angle -= math.pi / 200
            if self.angle < self.min_angle:
                self.angle = self.min_angle

    def trigger(self):
        self.triggered = True
    
    def segment(self):
        return segment(self.pivot, self.extreme(), self.color)
    
    def draw(self, screen):
        self.segment().draw(screen)
        pygame.draw.circle(screen, self.color, (self.pivot.x, self.pivot.y), 8)
        extreme = self.extreme().int()
        pygame.draw.circle(screen, self.color, (extreme.x, extreme.y), 5)
        angle1 = self.ang1()
        angle2 = angle1 + math.pi
        ext11 = self.pivot + vector(math.cos(angle1), math.sin(angle1)) * 8
        ext12 = self.pivot + vector(math.cos(angle2), math.sin(angle2)) * 8
        ext21 = extreme + vector(math.cos(angle1), math.sin(angle1)) * 5
        ext22 = extreme + vector(math.cos(angle2), math.sin(angle2)) * 5
        pygame.draw.line(screen, self.color, ext11.to_tuple(), ext21.to_tuple())
        pygame.draw.line(screen, self.color, ext12.to_tuple(), ext22.to_tuple())


class left_finger(finger):

    def extreme(self):
        return self.pivot + vector_angle(self.angle, self.length)

    def ang1(self):
        return -self.angle + math.pi / 2

class right_finger(finger):

    def extreme(self):
        return self.pivot + vector_angle(self.angle, self.length).horizontal_mirror()

    def ang1(self):
        return self.angle + math.pi / 2
