from random import random, choice
from enum import Enum

import entity
import game_loop
import variables
from player import Y_SPEED

W = 25
H = 5
DESPAWN_DISTANCE = 100
CLOSEST_LEGAL_DISTANCE = 100


class FloorType(Enum):
    MOVING = 0
    NORMAL = 1
    BOUNCY = 2


floor_types_list = list(FloorType)
floors = {
    FloorType.NORMAL: lambda x, y: Floor(x, y),
    FloorType.MOVING: lambda x, y: MovingFloor(x, y),
    FloorType.BOUNCY: lambda x, y: BouncyFloor(x, y)
}
floor_odds = {
    FloorType.NORMAL: 0.7,
    FloorType.MOVING: 0.2,
    FloorType.BOUNCY: 0.1
}


class Floor(entity.Entity):

    def __init__(self, x, y):
        super().__init__(x, y, W, H)

    def update(self, dt):
        if self.screen_pos()[1] > game_loop.screen.get_size()[1] + DESPAWN_DISTANCE:
            game_loop.floors.remove(self)

    def player_bounce(self, player):
        player.vy = Y_SPEED


class MovingFloor(Floor):
    right: bool

    def __init__(self, x, y):
        super().__init__(x, y)
        self.right = random() > 0.5

    def update(self, dt):
        super().update(dt)
        self.x += dt * 100 if self.right else -dt * 100

        if self.x > variables.SCREEN_SIZE[0] - 100 and self.right:
            self.right = False
        elif self.x < 100:
            self.right = True


class BouncyFloor(Floor):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.set_color(variables.GREEN)

    def player_bounce(self, player):
        player.vy = Y_SPEED * 3


def random_floor_type():
    num = random()
    cur_value = 0
    for key, value in floor_odds.items():
        cur_value += value
        if num < cur_value:
            return key


def spawn_floor(bounds: (float, float, float, float), _type=FloorType.NORMAL):
    x = random() * (bounds[1] - bounds[0] - W) + bounds[0]
    y = random() * (bounds[3] - bounds[2] - H) + bounds[2]
    return floors[_type](x, y)
