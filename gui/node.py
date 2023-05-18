from copy import deepcopy
import utils

class State:
    def __init__(self, board, move=None):
        if type(board) != list:
            self.board = board.board
        else:
            self.board = board
        self.move = move

    def get_children(self, max_player):
        curr = deepcopy(self.board)
        avail_moves = []
        children = []

        if max_player:
            avail_moves = utils.possible_moves(curr)
        else:
            avail_moves = utils.possible_moves(curr, False)
        for i in range(len(avail_moves)):
            current_pos = avail_moves[i][0]
            new_pos = avail_moves[i][1]
            state = deepcopy(curr)
            state[current_pos[0]][current_pos[1]].move(new_pos[0], new_pos[1])
            children.append(State(state, [current_pos, new_pos]))
        return children

    def get_board(self):
        return self.board