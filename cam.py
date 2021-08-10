import pygame
import entity
import game_loop
from player import FALL_DISTANCE


class Cam:
    y: float

    def __init__(self):
        self.y = 0

    def update(self):
        h = game_loop.screen.get_size()[1]
        y = game_loop.player.screen_pos()[1]
        if y < 100:
            self.y -= 100 - y
        elif y > h - 100 and game_loop.player.y - FALL_DISTANCE < game_loop.player.ymin:
            self.y += y - h + 100

    def draw(self, bg: pygame.Surface, e: entity.Entity):
        bg.blit(e.img, (e.x, e.y - self.y))

    def to_screen_point(self, world_point):
        return world_point[0], world_point[1] - self.y

    def to_world_point(self, screen_point):
        return screen_point[0], screen_point[1] + self.y


def lerp(a, b, t):
    return a + (b - a) * t
