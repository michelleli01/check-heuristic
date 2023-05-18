import math
from node import State
from copy import deepcopy

class Algo:
    def __init__(self, c_pieces, p_pieces, board):
        self.c_pieces = c_pieces
        self.p_pieces = p_pieces
        self.board = board

    def minimax(self, board, n, a, b, max_player):
        if n == 0:
            return Algo.calculate_heuristics(self, board)

        curr = State(deepcopy(self.board))
        if max_player == True:
            max_eval = -math.inf
            for c in curr.get_children(True):
                ev = Algo.minimax(self, c.get_board(), n-1, a, b, False)
                max_eval = max(max_eval, ev)
                a = max(a, ev)
                if b <= a:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for c in curr.get_children(False):
                ev = Algo.minimax(self, c.get_board(), n-1, a, b, True)
                min_eval = min(min_eval, ev)
                b = min(b, ev)

                if b <= a:
                    break
        return min_eval

    def calculate_heuristics(self, board):
        """
        Calculates heuristic/score used for minimax algorithm
        """
        all_kings = True
        while all_kings == True:
            for row in range(8):
                for col in range(8):
                    if board[row][col] != 0 and board[row][col].king == False:
                        all_kings = False
        if all_kings:
            if self.p_pieces > self.c_pieces:
                return Algo.distance_heuristic(board)
            else:
                return Algo.distance_heuristic(board) * -1
        else:
            return Algo.piece_heuristic(board) + Algo.piece_board_heuristic(board)

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
                if board[row][col] != 0:
                    if board[row][col].color == (255, 255, 255):    # curr pawn
                        curr += 1
                    elif board[row][col].color == (255, 255, 255) and board[row][col].king:  # curr king
                        curr += 2
                    elif board[row][col].color == (255, 0, 0):  # opp pawn
                        opp += 1
                    elif board[row][col].color == (255, 0, 0) and board[row][col].king:  # opp king
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
                if board[row][col] != 0:
                    if board[row][col].color == (255, 255, 255):   # curr pawn
                        if row < 4:                  # if curr pawn is in opponent's half
                            curr += 3
                        else:                        # if curr pawn is in its own half
                            curr += 2
                    elif board[row][col].color == (255, 255, 255) and board[row][col].king:  # curr king
                        curr += 5
                    if board[row][col].color == (255, 0, 0):   # opp pawn
                        if row >= 4:                 # if opponent's pawn is in current player's half
                            curr += 3
                        else:                        # if opponent's pawn is in its own half
                            opp += 2
                    elif board[row][col].color == (255, 0, 0) and board[row][col].king:  # opp king
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
                if board[row][col] != 0:
                    if board[row][col].color == (255, 255, 255) and board[row][col].king:
                        curr_lst.append((row, col))
                    elif board[row][col].color == (255, 0, 0) and board[row][col].king:
                        opp_lst.append((row, col))

        # calculate distances over all pieces
        for x in curr_lst:
            for o in opp_lst:
                dist += math.dist(x, o)

        return dist