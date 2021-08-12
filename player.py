import pygame

import entity
import game_loop
from variables import G

X_SPEED = 150
Y_SPEED = 400
FALL_DISTANCE = 300


class Player(entity.Entity):
    vx: float
    vy: float
    ymin: float
    score: int

    def __init__(self, x, y):
        super().__init__(x, y)
        self.vx = self.vy = 0
        self.ymin = y
        self.score = 0

    def update(self, dt):
        self.ymin = min(self.ymin, self.y)

        self.vy += G * dt
        if self.vy < 0:
            self.check_floor_collisions()

        self.x += self.vx * dt
        self.y -= self.vy * dt

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.vx = X_SPEED
        elif keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            self.vx = -X_SPEED
        else:
            self.vx = 0

        if self.y > game_loop.cam.y + 700:
            game_loop.lost = True

        self.score = int(-self.ymin / 100) + 1

    def check_floor_collisions(self):
        for floor in game_loop.floors:
            if self.bottom_intersects(floor):
                floor.player_bounce(self)

    def bottom_intersects(self, other):
        return self.x + self.w > other.x and self.x < other.x + other.w \
               and other.y < self.y + self.h < other.y + other.h
