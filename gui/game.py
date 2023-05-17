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
        self.comp_playing = False

    def winner(self):
        return self.board.winner()

    def select(self, row, col):
        if self.selected != None:
            result = self.move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.player:
            self.selected = piece
            self.moves = self.board.get_possible_moves(piece, self.comp_playing)
            return True

        return False

    def move(self, row, col):
        piece = self.board.get_piece(row, col)
        selected_piece = self.board.get_piece(self.selected.row, self.selected.col)

        diffR = selected_piece.row - row
        diffC = selected_piece.col - col

        if self.selected != None and piece == 0 and [(selected_piece.row, selected_piece.col), (row, col)] in self.moves:
            self.board.move(self.selected, row, col)

            jump = None

            if diffR == -2 and diffC == 2:
                jump = [self.board.get_piece(selected_piece.row + 1, selected_piece.col -1)]
            elif diffR == 2 and diffC == 2:
                jump = [self.board.get_piece(selected_piece.row - 1, selected_piece.col -1)]
            elif diffR == 2 and diffC == -2:
                jump = [self.board.get_piece(selected_piece.row - 1, selected_piece.col +1)]
            elif diffR == -2 and diffC == -2:
                jump = [self.board.get_piece(selected_piece.row + 1, selected_piece.col +1)]

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
            newRow = move[1][0]
            newCol = move[1][1]
            pygame.draw.circle(self.screen, (0, 0, 255), (newCol*100 + 100//2, newRow * 100 + 100//2), 15)

    def switch_player(self):
        self.moves = []
        if self.player == (255, 0, 0):
            self.player = (255, 255, 255)
            self.comp_playing = False
        else:
            self.player = (255, 0, 0)
            self.comp_playing = True


    def get_board(self):
        return self.board

    def comp_move(self, board):
        self.board = board
        self.switch_player()