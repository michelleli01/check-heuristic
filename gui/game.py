import pygame
from board import Board

class Game:
    def __init__(self, screen):
        self.reset()
        self.screen = screen

    def reset(self):
        self.selected = None
        self.board = Board()
        self.player = (255, 255, 255)
        self.moves = []

    def winner(self):
        return self.board.winner()

    def select(self, row, col):
        if self.selected:
            result = self.move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.player:
            self.selected = piece
            self.valid_moves = self.board.get_possible_moves(piece)
            return True

        return False

    def move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.moves:
            self.board.move(self.selectd, row, col)
            jump = self.moves[(row, col)]
            if jump:
                self.board.remove(jump)
            self.switch_player()

        else:
            return False

        return True

    def update(self):
        self.board.draw(self.screen)
        self.draw_valid_moves(self.moves)
        pygame.display.update()

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.screen, (0, 0, 255), (col*100 + 100//2, row * 100 + 100//2), 15)

    def switch_player(self):
        self.moves = []
        if self.player == (255, 0, 0):
            self.player = (255, 255, 255)
        else:
            self.turn = (255, 0, 0)

    def get_board(self):
        return self.board

    def comp_move(self, board):
        self.board = board
        self.switch_player()