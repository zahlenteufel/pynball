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

        self.ball = Ball(Vector(150, 450), 10, Vector(0, 0))

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
                self.ball.center = Vector(*pos)

    def draw(self):
        self.screen.fill(BLACK)

        for segment in self.segments:
            segment.draw(self.screen)

        self.left_finger.draw(self.screen)
        # self.right_finger.draw(self.screen)

        self.ball.draw(self.screen)

    def get_collision_time(self, ball, finger, t):
        t0 = 0
        t1 = t
        ball0 = ball
        finger0 = finger
        while t1 - t0 > 0.0001:
            ## at t0 => not collidingzz
            ## at t1 => colliding
            mid = (t0 + t1) / 2
            ball = ball0.at(mid)
            finger = finger0.at(mid)
            if finger.collides(ball):
                t1 = mid
            else:
                t0 = mid
        return mid

    def simulate_physics(self):
        dt = 1.0
        for i in xrange(10):
            # assert(not self.left_finger.collides(self.ball))
            ball_next = self.ball.at(dt)
            lfingernext = self.left_finger.at(dt)
            #
            if lfingernext.collides(ball_next):
                collision_time = self.get_collision_time(
                    self.ball, self.left_finger, dt)
                ball_next = self.ball.at(collision_time)
                lfingercollision = self.left_finger.at(collision_time)
                ball_next = lfingercollision.impact_on(ball_next)
                ball_next = ball_next.at(dt - collision_time)
                lfingernext = self.left_finger.at(dt)

            self.left_finger = lfingernext
            self.ball = ball_next

            self.ball.apply_colissions_to_segments(self.segments)

    def game_loop(self):
        while True:
            self.process_events()
            self.simulate_physics()
            self.draw()
            pygame.display.flip()

            self.clock.tick(self.FPS)


if __name__ == "__main__":
    pynball = Pynball()
