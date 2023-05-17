import math
from node import State
from copy import deepcopy

def minimax(board, n, a, b, max_player):
  if n == 0:
      return calculate_heuristics(board)

  curr = State(deepcopy(board))
  if max_player == True:
      max_eval = -math.inf
      for c in curr.get_children(True):
          ev = minimax(c.get_board(), n-1, a, b, False)
          max_eval = max(max_eval, ev)
          a = max(a, ev)
          if b <= a:
              break
      return max_eval
  else:
      min_eval = math.inf
      for c in curr.get_children(False):
          ev = minimax(c.get_board(), n-1, a, b, True)
          min_eval = min(min_eval, ev)
          b = min(b, ev)

          if b <= a:
              break
      return min_eval

def calculate_heuristics(p_pieces, c_pieces, board):
  """
  Calculates heuristic/score used for minimax algorithm
  """
  all_kings = True
  while all_kings == True:
      for row in range(8):
          for col in range(8):
              if board[row][col] == " x " or board[row][col] == " o ":
                  all_kings = False
  if all_kings:
      if p_pieces > c_pieces:
          return distance_heuristic(board)
      else:
          return distance_heuristic(board) * -1
  else:
      return piece_heuristic(board) + piece_board_heuristic(board)

def piece_heuristic(board):
  """
  Assign value to each piece based on type of piece
  King = 2
  Pawn = 1

  Returns total sum for current player - total sum for opponent (Player is
  winning if sum > 0)
  """
  curr = 0  # current player is x
  opp = 0  # opponent (computer) is o

  for row in range(8):
      for col in range(8):
          if board[row][col] == " x ":    # curr pawn
              curr += 1
          elif board[row][col] == " X ":  # curr king
              curr += 2
          elif board[row][col] == " o ":  # opp pawn
              opp += 1
          elif board[row][col] == " O ":  # opp king
              opp += 2

  return curr - opp

def piece_board_heuristic(board):
  """
  Assign value to each piece based on type of piece and position on board
  King = 5
  Pawn in opponent half of board = 3
  Pawn in player half of board = 2

  Returns total sum for current player - total sum for opponent (Player is
  winning if sum > 0)
  """
  curr = 0  # current player is x
  opp = 0  # opponent (computer) is o

  for row in range(8):
      for col in range(8):
          if board[row][col] == " x ":   # curr pawn
              if row < 4:                  # if curr pawn is in opponent's half
                  curr += 3
              else:                        # if curr pawn is in its own half
                  curr += 2
          elif board[row][col] == " X ":  # curr king
              curr += 5
          if board[row][col] == " o ":   # opp pawn
              if row >= 4:                 # if opponent's pawn is in current player's half
                  curr += 3
              else:                        # if opponent's pawn is in its own half
                  opp += 2
          elif board[row][col] == " O ":  # opp king
              opp += 5

  return curr - opp

def distance_heuristic(board):
  """
  Use only when all pieces on board are kings!

  For each piece sum all distances from that piece to each of the opponent’s pieces
  If the current player has more kings than opponent, a smaller distance is
  preferred (attack)
  If the current player has fewer kings than opponent, a greater distance is
  preferred (defense)

  Returns total sum of distances over all pieces for current player
  """
  dist = 0

  curr_lst = []  # list containing positions of all current player kings
  opp_lst = []  # list containing positions of all opponent kings
  for row in range(8):
      for col in range(8):
          if board[row][col] == " X ":
              curr_lst.append((row, col))
          elif board[row][col] == " O ":
              opp_lst.append((row, col))

  # calculate distances over all pieces
  for x in curr_lst:
      for o in opp_lst:
          dist += math.dist(x, o)

  return dist