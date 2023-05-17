import pygame

TILE_SIZE = 100
CROWN = pygame.transform.scale(pygame.image.load("images/crown.png"), (50, 25))

class Piece:
    def __init__ (self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = TILE_SIZE * self.col + TILE_SIZE // 2
        self.y = TILE_SIZE * self.row + TILE_SIZE // 2

    def king(self):
        self.king = True

    def draw(self, screen):
        radius = TILE_SIZE // 2 - 20
        pygame.draw.circle(screen, self.color, (self.x, self.y), radius)

        if self.king:
            screen.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.x = TILE_SIZE * self.col + TILE_SIZE // 2
        self.y = TILE_SIZE * self.row + TILE_SIZE // 2