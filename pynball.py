import pygame
import sys
import math
from vector import Vector
from segment import Segment
from ball import Ball
from finger import LeftFinger, RightFinger

BLACK = (0, 0, 0)
DARK_GREEN = (128, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


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


class Pynball:

    WIDTH = 400
    HEIGHT = 600
    FPS = 40

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT), 0, 32)
        self.clock = pygame.time.Clock()

        exterior_walls = segments_from_rectangle(
            -1, -1, self.WIDTH + 2, self.HEIGHT + 2, DARK_GREEN)

        obstacles = \
            [
                Segment(Vector(50, 450), Vector(140, 530), DARK_GREEN),
                Segment(Vector(260, 530), Vector(320, 475), DARK_GREEN)
            ]

        self.segments = exterior_walls + obstacles

        self.left_finger = LeftFinger(
            Vector(140, 540), 40, -math.pi / 4, math.pi / 4, RED)

        self.right_finger = RightFinger(
            Vector(260, 540), 40, -math.pi / 4, math.pi / 4, YELLOW)

        self.ball = Ball(Vector(150, 200), 10, Vector(0, 0))

        pygame.display.set_caption("Pynball")

        self.game_loop()

    def should_quit(self, event):
        return event.type == pygame.QUIT or \
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE

    def process_events(self):
        for event in pygame.event.get():
            if self.should_quit(event):
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    self.left_finger.push()
                elif event.key == pygame.K_m:
                    self.right_finger.push()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_z:
                    self.left_finger.release()
                elif event.key == pygame.K_m:
                    self.right_finger.release()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                self.ball.center = Vector(pos[0], pos[1])

    def draw(self, screen):
        screen.fill(BLACK)

        for segment in self.segments:
            segment.draw(screen)

        self.left_finger.draw(screen)
        self.right_finger.draw(screen)

        self.ball.draw(screen)

    def simulate_physics(self):
        for i in xrange(10):
            self.ball.apply_gravity()
            self.left_finger.update_move()
            self.right_finger.update_move()
            self.ball.apply_colissions(
                self.segments +
                self.left_finger.segments() +
                self.right_finger.segments())

    def game_loop(self):
        while True:
            self.process_events()
            self.simulate_physics()
            self.draw(self.screen)
            pygame.display.flip()

            self.clock.tick(self.FPS)


if __name__ == "__main__":
    pynball = Pynball()
