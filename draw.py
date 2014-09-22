import pygame


def draw_line(screen, p1, p2, color):
    pygame.draw.line(screen, color, p1.int().tuple(), p2.int().tuple(), 1)


def draw_arrow(screen, p1, p2):
    pygame.draw.line(
        screen,
        (255, 255, 255),
        p1.int().tuple(),
        p2.int().tuple(),
        1
    )
    draw_circle(screen, (255, 255, 255), p2, 2)


def draw_circle(screen, color, center, radius):
    pygame.draw.circle(screen, color, center.int().tuple(), int(radius), 1)
