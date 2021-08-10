from random import random

import entity
import game_loop

W = 25
H = 5
DESPAWN_DISTANCE = 100
CLOSEST_LEGAL_DISTANCE = 100


class Floor(entity.Entity):

    def __init__(self, x, y):
        super().__init__(x, y, W, H)

    def update(self):
        if self.screen_pos()[1] > game_loop.screen.get_size()[1] + DESPAWN_DISTANCE:
            game_loop.floors.remove(self)


def spawn_floor(bounds: (float, float, float, float)):
    x = random() * (bounds[1] - bounds[0] - W) + bounds[0]
    y = random() * (bounds[3] - bounds[2] - H) + bounds[2]
    floor = Floor(x, y)
    return floor if len([f for f in game_loop.floors if f.sqr_dist(floor) < CLOSEST_LEGAL_DISTANCE]) == 0 else \
        spawn_floor(bounds)
