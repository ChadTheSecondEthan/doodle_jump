import sys
import pygame
from time import perf_counter

import floor
import variables
from cam import Cam
from floor import spawn_floor
from player import Player

background: pygame.Surface
screen: pygame.display
font: pygame.font.Font
player: Player
floors: []
cam: Cam
prev_time: float

lose_text: pygame.Surface
lose_text_pos: (float, float)

score_text: pygame.Surface
score_text_pos: (float, float)

lost = False


def start(s):
    global background, screen, player, cam, floors, prev_time, lose_text, lose_text_pos, font

    screen = s

    background = pygame.Surface(variables.SCREEN_SIZE)
    background = background.convert()

    x, y = variables.SCREEN_SIZE
    x = (x - 10) / 2
    y = (y - 10) / 2
    player = Player(x, y)

    cam = Cam()
    floors = []

    for i in range(10):
        floors.append(floor.spawn_floor((0, variables.SCREEN_SIZE[0], 0, variables.SCREEN_SIZE[1])))

    font = pygame.font.SysFont("Sans Serif", 48, False, False)

    lose_text = font.render("You lost", False, variables.WHITE)
    lose_text_pos = (variables.HALF_SCREEN_SIZE[0] - lose_text.get_size()[0] / 2, variables.HALF_SCREEN_SIZE[1] -
                     lose_text.get_size()[1] / 2)

    prev_time = perf_counter()


def update():
    global score_text, score_text_pos

    background.fill(variables.BG_COLOR)

    if pygame.key.get_pressed()[pygame.K_ESCAPE]:
        sys.exit()

    if lost:
        update_lose()
    else:
        update_game()

    score_text = font.render("Score: " + str(player.score), False, variables.WHITE)
    score_text_pos = (variables.HALF_SCREEN_SIZE[0] - lose_text.get_size()[0] / 2, variables.HALF_SCREEN_SIZE[1] -
                     lose_text.get_size()[1] / 2 + 200)

    screen.blit(background, (0, 0))
    pygame.display.flip()


def update_game():
    global prev_time

    dt = perf_counter() - prev_time

    player.update(dt)
    for _floor in floors:
        _floor.update()
    cam.update()

    floors_in = floors_in_range(cam.y, cam.y - 50)
    if len(floors_in) == 0:
        floors.append(spawn_floor((0, variables.SCREEN_SIZE[0], cam.y, cam.y - 50)))

    cam.draw(background, player)
    for _floor in floors:
        cam.draw(background, _floor)
    background.blit(score_text, score_text_pos)

    prev_time = perf_counter()


def update_lose():
    background.blit(lose_text, lose_text_pos)


def floors_in_range(y1, y2):
    y_min = min(y1, y2)
    y_max = max(y1, y2)
    floors_in = []
    for _floor in floors:
        if y_min < _floor.y < y_max:
            floors_in.append(_floor)
    return floors_in
