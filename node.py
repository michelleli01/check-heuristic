from copy import deepcopy

class Node:
    def __init__(self, board, move=None, val=None):
        self.board = board
        self.val = val
        self.move = move

    def get_children(self, max_player):
        curr = deepcopy(self.board)
        avail_moves = []
        children = []

        if max_player:
            avail_moves = Checkers.possible_moves(curr)
        else:
            avail_moves = Checkers.possible_moves(curr, False)
        for i in range(len(avail_moves)):
            current_pos = avail_moves[i][0]
            new_pos = avail_moves[i][1]
            state = deepcopy(curr)
            Checkers.move_piece(state, current_pos, new_pos)
            children.append(Node(state, [current_pos, new_pos]))
        return children

    def set_value(self, val):
        self.val = val

    def get_board(self):
        return self.board