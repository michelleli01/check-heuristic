import pygame
from piece import Piece
# from node import State
from copy import deepcopy
import time
import math
import algo as algo

class Board:
  def __init__(self):
      self.board =  [[], [], [], [], [], [], [], []]
      self.c_pieces = self.p_pieces = 12
      self.create_board()

  def draw_squares(self, screen):
      screen.fill((0, 0, 0))
      for row in range(8):
          for col in range(row % 2, 8, 2):
              pygame.draw.rect(screen, (255, 0, 0), (row*100, col *100, 100, 100))

  def evaluate(self):
      t = time.time()
    #   curr = State(deepcopy(self.board))
    #   c_moves = curr.get_children(True)
    #   if len(c_moves) == 0:
    #       if self.p_pieces > self.c_pieces:
    #           print("You have more pieces than the computer. YOU WIN")
    #           exit()
    #       else:
    #           print("Computer has no available moves left. DRAW")
    #           exit()

    #   d = dict()
    #   for i in range(len(c_moves)):
    #       c = c_moves[i]
    #       val = algo.minimax(self, c.get_board(), 5, -math.inf, math.inf, False)
    #       d[val] = c

    #   if len(d.keys()) == 0:
    #       print("Computer has cornered itself. YOU WIN")
    #       exit()
    #   n_board = d[max(d)].get_board()
    #   move = d[max(d)].move
    #   self.board = n_board

    #   t1 = time.time()
    #   diff = t1-t

    #   print(
    #       f"Computer moved from '{str(move[0][0]), str(move[0][1])}' to '{str(move[1][0]), str(move[1][1])}'")
    #   print(
    #       f"Total time taken for computer to make move: {str(diff)} seconds")

  def get_all_pieces(self, color):
      pieces = []
      for row in self.board:
          for piece in row:
              if piece != 0 and piece.color == color:
                  pieces.append(piece)
      return pieces

  def move(self, piece, row, col):
      self.board[piece.row][piece.col] = self.board[row][col]
      self.board[row][col] = self.board[piece.row][piece.col]
      piece.move(row, col)

      if row == 7 or row == 0:
          piece.king()

  def get_piece(self, row, col):
      return self.board[row][col]

  def create_board(self):
      for row in range(8):
          self.board.append([])
          for col in range(8):
              if col % 2 == ((row +  1) % 2):
                  if row > 4:
                      self.board[row].append(Piece(row, col, (255, 255, 255)))
                  elif row < 3:
                      self.board[row].append(Piece(row, col, (255, 0, 0)))
                  else:
                      self.board[row].append(0)
              else:
                  self.board[row].append(0)

  def draw(self, screen):
      self.draw_squares(screen)
      for row in range(8):
          for col in range(8):
              piece = self.board[row][col]
              if piece != 0:
                  piece.draw(screen)

  def remove_piece(self, pieces):
      for piece in pieces:
          self.board[piece.row][piece.col] = 0
          if piece != 0:
              if piece.color == (255, 0, 0):
                  self.c_pieces -= 1
              else:
                  self.p_pieces -= 1

  def valid(self, current_pos, new_pos, eat, comp_playing):
      cR = current_pos[0]
      cC = current_pos[1]
      nR = new_pos[0]
      nC = new_pos[1]
      if nR > 7 or nR < 0:
          return False
      if nC > 7 or nC < 0:
          return False
      if self.board[cR][cC] == "   ":
          return False
      if self.board[nR][nC] != "   ":
          return False
      if comp_playing:
          if self.board[cR][cC] == " x " or self.board[cR][cC] == " X ":
              return False
      if not comp_playing:
          if self.board[cR][cC] == " o " or self.board[cR][cC] == " O ":
              return False
      if eat == (-1, -1):
          return self.board[nR][nC] == "   "
      else:
          return self.jump(self, current_pos, new_pos, eat)

  def jump(self, current_pos, new_pos, eat=(-1, -1)):
      cR = current_pos[0]
      cC = current_pos[1]
      takeR = eat[0]
      takeC = eat[1]
      if self.board[takeR][takeC] == "   ":
          return False
      if self.board[cR][cC] == " O " or self.board[cR][cC] == " o ":
          if self.board[takeR][takeC] == " X " or self.board[takeR][takeC] == " x ":
              return True
      if self.board[cR][cC] == " X " or self.board[cR][cC] == " x ":
          if self.board[takeR][takeC] == " O " or self.board[takeR][takeC] == " o ":
              return True
      return False

  def possible_moves(self, comp_playing):
      moves = []
      for r in range(8):
          for c in range(8):
              if comp_playing:
                  if self.board[r][c].color == (255, 255, 255) or self.board[r][c].king:
                      if self.valid(self, (r, c), (r + 1, c + 1), (-1, -1), comp_playing):
                          moves.append([(r, c), (r + 1, c + 1)])
                      if self.valid(self, (r, c), (r + 1, c - 1), (-1, -1), comp_playing):
                          moves.append([(r, c), (r + 1, c - 1)])
                      if self.valid(self, (r, c), (r + 2, c - 2), (r+1, c-1), comp_playing):
                          moves.append([(r, c), (r + 2, c - 2)])
                      if self.valid(self, (r, c), (r + 2, c + 2), (r+1, c+1), comp_playing):
                          moves.append([(r, c), (r + 2, c + 2)])
                  if self.board[r][c].king:
                      if self.valid(self, (r, c), (r - 1, c - 1), (-1, -1), comp_playing):
                          moves.append([(r, c), (r - 1, c - 1)])
                      if self.valid(self, (r, c), (r - 1, c + 1), (-1, -1), comp_playing):
                          moves.append([(r, c), (r - 1, c + 1)])
                      if self.valid(self, (r, c), (r - 2, c - 2), (r-1, c-1), comp_playing):
                          moves.append([(r, c), (r - 2, c - 2)])
                      if self.valid(self, (r, c), (r - 2, c + 2), (r-1, r+1), comp_playing):
                          moves.append([(r, c), (r - 2, c + 2)])
              if not comp_playing:
                  if self.board[r][c].color == (255, 0, 0) or self.board[r][c].king:
                      if self.valid(self, (r, c), (r - 1, c - 1), (-1, -1), comp_playing):
                          moves.append([(r, c), (r - 1, c - 1)])
                      if self.valid(self, (r, c), (r - 1, c + 1), (-1, -1), comp_playing):
                          moves.append([(r, c), (r - 1, c + 1)])
                      if self.valid(self, (r, c), (r - 2, c - 2), (r-1, c-1), comp_playing):
                          moves.append([(r, c), (r - 2, c - 2)])
                      if self.valid(self, (r, c), (r - 2, c + 2), (r-1, c+1), comp_playing):
                          moves.append([(r, c), (r - 2, c + 2)])
                  if self.board[r][c].king:
                      if self.valid(self, (r, c), (r + 1, c - 1), (-1, -1), comp_playing):
                          moves.append([(r, c), (r + 1, c - 1)])
                      if self.valid(self, (r, c), (r + 1, c + 1), (-1, -1), comp_playing):
                          moves.append([(r, c), (r + 1, c + 1)])
                      if self.valid(self, (r, c), (r + 2, c - 2), (r+1, c-1), comp_playing):
                          moves.append([(r, c), (r + 2, c - 2)])
                      if self.valid(self, (r, c), (r + 2, c + 2), (r+1, c+1), comp_playing):
                          moves.append([(r, c), (r + 2, c + 2)])

      return moves

