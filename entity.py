import math
import pygame

import game_loop
import variables


class Entity:
    x: float
    y: float
    w: float
    h: float
    img: pygame.Surface

    def __init__(self, x=0, y=0, w=10, h=10):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.img = pygame.Surface((w, h)).convert()
        self.set_color(variables.WHITE)

    def set_color(self, color):
        self.img.fill(color)

    def intersects(self, other):
        return self.x + self.w > other.x and self.x < other.x + other.w \
               and self.y + self.h > other.y and self.y < other.y + other.h

    def screen_pos(self):
        return self.x, self.y - game_loop.cam.y

    def sqr_dist(self, other):
        return (other.x - self.x) ** 2 + (other.y - self.y) ** 2

    def distance(self, other):
        return math.sqrt(self.sqr_dist(other))
