import pygame

CROWN_IMG = pygame.transform.scale(pygame.image.load("images/crown.png"), (50, 25))

class Piece:
    def __init__ (self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 100 * self.col + 100 // 2
        self.y = 100 * self.row + 100 // 2

    def king(self):
        self.king = True

    def draw_piece(self, screen):
        radius = 100 // 2 - 20
        pygame.draw.circle(screen, self.color, (self.x, self.y), radius)

        if self.king:
            screen.blit(CROWN_IMG, (self.x - CROWN_IMG.get_width()//2, self.y - CROWN_IMG.get_height()//2))

    def move(self, row, col):
        self.row = row
        self.col = col
        self.x = 100 * self.col + 100 // 2
        self.y = 100 * self.row + 100 // 2