from copy import deepcopy
# from board import Board

class State:
    def __init__(self, board, move=None):
        self.board = board
        self.move = move

    def get_children(self, max_player):
        curr = deepcopy(self.board)
        avail_moves = []
        children = []

        if max_player:
            avail_moves = Board.possible_moves(curr)
        else:
            avail_moves = Board.possible_moves(curr, False)
        for i in range(len(avail_moves)):
            current_pos = avail_moves[i][0]
            new_pos = avail_moves[i][1]
            state = deepcopy(curr)
            Board.move_piece(state, current_pos, new_pos)
            children.append(State(state, [current_pos, new_pos]))
        return children

    def get_board(self):
        return self.board