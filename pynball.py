import pygame
import sys
import levels
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

    FPS = 40

    def __init__(self, level):
        self.load_level(level)
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height), 0, 32)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Pynball")
        self.game_loop()

    def load_level(self, level):
        self.width = level['size']['width']
        self.height = level['size']['height']

        exterior_walls = segments_from_rectangle(
            -1, -1, self.width + 2, self.height + 2, DARK_GREEN)

        self.segments = exterior_walls

        for obstacle in level['obstacles']:
            self.segments.append(
                Segment(
                    Vector(*obstacle['from']),
                    Vector(*obstacle['to']),
                    DARK_GREEN
                )
            )

        lfinger = level['fingers'][0]  # just for now..
        rfinger = level['fingers'][1]

        self.left_finger = \
            LeftFinger(
                Vector(*lfinger['pivot']),
                lfinger['length'],
                lfinger['min_angle'],
                lfinger['max_angle'],
                lfinger['color']
            )

        self.right_finger = \
            RightFinger(
                Vector(*rfinger['pivot']),
                rfinger['length'],
                rfinger['min_angle'],
                rfinger['max_angle'],
                rfinger['color']
            )

        self.ball = Ball(
            Vector(*level['ball']['position']),
            level['ball']['radius'],
            Vector(*level['ball']['velocity'])
        )

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
        if self.left_finger.collides(self.ball):
            return 0
        t0 = 0
        t1 = t
        ball0 = ball
        finger0 = finger
        while t1 - t0 > 0.0001:
            ## at t0 => not colliding
            ## at t1 => colliding
            mid = (t0 + t1) / 2
            ball = ball0.at(mid)
            finger = finger0.at(mid)
            if finger.collides(ball):
                t1 = mid
            else:
                t0 = mid
        assert(not finger0.at(t0).collides(ball0.at(t0)))
        assert(finger0.at(t1).collides(ball0.at(t1)))
        return t1

    def simulate_physics(self):
        dt = 1.0
        for i in xrange(10):
            # assert(not self.left_finger.collides(self.ball))
            ball_next = self.ball.at(dt)
            lfingernext = self.left_finger.at(dt)
            #
            if lfingernext.collides(ball_next):
                # print "begin collision"
                collision_time = self.get_collision_time(
                    self.ball, self.left_finger, dt)
                ball_next = self.ball.at(collision_time)
                lfingercollision = self.left_finger.at(collision_time)
                ball_next = lfingercollision.impact_on(ball_next)
                ball_next = ball_next.at(dt - collision_time)
                lfingernext = self.left_finger.at(dt)
                # print "end collision"

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
    pynball = Pynball(levels.standard)
