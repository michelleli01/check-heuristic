import pygame
from game import Game
import algo
import math

WIDTH = 800
HEIGHT = 800
TILE_SIZE = 100

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

CROWN = pygame.transform.scale(pygame.image.load("images/crown.png"), (50, 25))

def get_position(pos):
    x, y = pos
    row = y // TILE_SIZE
    col = x // TILE_SIZE

    return row, col

def main():
    playing = True
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Check-heuristic")

    game = Game(screen)

    while playing:
        clock.tick(60)
        # board.draw(screen=screen)
        # pygame.display.flip()

        # if game.player == (255, 0, 0):
        #     val = algo.minimax(game.get_board(), 5, -math.inf, math.inf, False)

        if game.winner() != None:
            print(game.winner())
            playing = False

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                playing = False

            if ev.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_position(pos)
                game.select(row, col)

        game.update()

    pygame.quit()

main()
