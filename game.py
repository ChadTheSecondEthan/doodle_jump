import sys
import pygame

import variables
import game_loop


def main():
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode(variables.SCREEN_SIZE)
    pygame.display.set_caption('Basic Pygame program')

    game_loop.start(screen)

    # Event loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        game_loop.update()


if __name__ == '__main__':
    main()
