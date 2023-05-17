from copy import deepcopy
import time
import math


class State:
    def __init__(self, board, move=None):
        self.board = board
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
            children.append(State(state, [current_pos, new_pos]))
        return children

    def get_board(self):
        return self.board


class Checkers:

    def __init__(self):
        self.board = [[], [], [], [], [], [], [], []]
        self.playing = True
        self.c_pieces = self.p_pieces = 12

    def setup_board(self):
        for row in self.board:
            for i in range(8):
                row.append("   ")
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    # lowercase o for pawn, uppercase O for king
                    self.board[row][col] = " o "
        for row in range(5, 8, 1):
            for col in range(8):
                if (row + col) % 2 == 1:
                    # lowercase x for pawn, uppercase X for king
                    self.board[row][col] = " x "

    def print_board(self):
        letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
        numbers = ["1", "2", "3", "4", "5", "6", "7", "8"]

        print("     " + "-"*33)

        for r in range(8):
            row = self.board[r]
            print(letters[r] + "    ", end="|")
            for i in row:
                print(i, end="|")

            print("")
        print("     " + "-"*33)

        nums = "     "
        for num in numbers:
            nums += "  " + str(num) + " "
        print(nums)

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

    def calculate_heuristics(self, board):
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
            if self.p_pieces > self.c_pieces:
                return Checkers.distance_heuristic(board)
            else:
                return Checkers.distance_heuristic(board) * -1
        else:
            return Checkers.piece_heuristic(board) + Checkers.piece_board_heuristic(board)

    def jump(board, current_pos, new_pos, eat=(-1, -1)):
        cR = current_pos[0]
        cC = current_pos[1]
        takeR = eat[0]
        takeC = eat[1]
        if board[takeR][takeC] == "   ":
            return False
        if board[cR][cC] == " O " or board[cR][cC] == " o ":
            if board[takeR][takeC] == " X " or board[takeR][takeC] == " x ":
                return True
        if board[cR][cC] == " X " or board[cR][cC] == " x ":
            if board[takeR][takeC] == " O " or board[takeR][takeC] == " o ":
                return True
        return False

    def valid(board, current_pos, new_pos, eat, comp_playing):
        cR = current_pos[0]
        cC = current_pos[1]
        nR = new_pos[0]
        nC = new_pos[1]
        if nR > 7 or nR < 0:
            return False
        if nC > 7 or nC < 0:
            return False
        if board[cR][cC] == "   ":
            return False
        if board[nR][nC] != "   ":
            return False
        if comp_playing:
            if board[cR][cC] == " x " or board[cR][cC] == " X ":
                return False
        if not comp_playing:
            if board[cR][cC] == " o " or board[cR][cC] == " O ":
                return False
        if eat == (-1, -1):
            return board[nR][nC] == "   "
        else:
            return Checkers.jump(board, current_pos, new_pos, eat)

    def possible_moves(board, comp_playing=True):
        moves = []
        for r in range(8):
            for c in range(8):
                if comp_playing:
                    if board[r][c] == " o " or board[r][c] == " O ":
                        if Checkers.valid(board, (r, c), (r + 1, c + 1), (-1, -1), comp_playing):
                            moves.append([(r, c), (r + 1, c + 1)])
                        if Checkers.valid(board, (r, c), (r + 1, c - 1), (-1, -1), comp_playing):
                            moves.append([(r, c), (r + 1, c - 1)])
                        if Checkers.valid(board, (r, c), (r + 2, c - 2), (r+1, c-1), comp_playing):
                            moves.append([(r, c), (r + 2, c - 2)])
                        if Checkers.valid(board, (r, c), (r + 2, c + 2), (r+1, c+1), comp_playing):
                            moves.append([(r, c), (r + 2, c + 2)])
                    if board[r][c] == " O ":
                        if Checkers.valid(board, (r, c), (r - 1, c - 1), (-1, -1), comp_playing):
                            moves.append([(r, c), (r - 1, c - 1)])
                        if Checkers.valid(board, (r, c), (r - 1, c + 1), (-1, -1), comp_playing):
                            moves.append([(r, c), (r - 1, c + 1)])
                        if Checkers.valid(board, (r, c), (r - 2, c - 2), (r-1, c-1), comp_playing):
                            moves.append([(r, c), (r - 2, c - 2)])
                        if Checkers.valid(board, (r, c), (r - 2, c + 2), (r-1, r+1), comp_playing):
                            moves.append([(r, c), (r - 2, c + 2)])
                if not comp_playing:
                    if board[r][c] == " x " or board[r][c] == " X ":
                        if Checkers.valid(board, (r, c), (r - 1, c - 1), (-1, -1), comp_playing):
                            moves.append([(r, c), (r - 1, c - 1)])
                        if Checkers.valid(board, (r, c), (r - 1, c + 1), (-1, -1), comp_playing):
                            moves.append([(r, c), (r - 1, c + 1)])
                        if Checkers.valid(board, (r, c), (r - 2, c - 2), (r-1, c-1), comp_playing):
                            moves.append([(r, c), (r - 2, c - 2)])
                        if Checkers.valid(board, (r, c), (r - 2, c + 2), (r-1, c+1), comp_playing):
                            moves.append([(r, c), (r - 2, c + 2)])
                    if board[r][c] == " X ":
                        if Checkers.valid(board, (r, c), (r + 1, c - 1), (-1, -1), comp_playing):
                            moves.append([(r, c), (r + 1, c - 1)])
                        if Checkers.valid(board, (r, c), (r + 1, c + 1), (-1, -1), comp_playing):
                            moves.append([(r, c), (r + 1, c + 1)])
                        if Checkers.valid(board, (r, c), (r + 2, c - 2), (r+1, c-1), comp_playing):
                            moves.append([(r, c), (r + 2, c - 2)])
                        if Checkers.valid(board, (r, c), (r + 2, c + 2), (r+1, c+1), comp_playing):
                            moves.append([(r, c), (r + 2, c + 2)])

        return moves

    def move_piece(board, current_pos, new_pos):

        cR = current_pos[0]
        cC = current_pos[1]
        nR = new_pos[0]
        nC = new_pos[1]
        diffR = cR - nR
        diffC = cC - nC

        letter = board[cR][cC]
        crown = " O "
        turn_row = 7

        if diffR == -2 and diffC == 2:
            board[cR+1][cC-1] = "   "
        elif diffR == 2 and diffC == 2:
            board[cR-1][cC-1] = "   "
        elif diffR == 2 and diffC == -2:
            board[cR-1][cC+1] = "   "
        elif diffR == -2 and diffC == 2:
            board[cR+1][cC+1] = "   "
        if letter == " x ":
            crown = " X "
            turn_row = 0
        if nR == turn_row:
            letter = crown
        board[cR][cC] = "   "
        board[nR][nC] = letter

    def get_input(self):
        # USER PLAYING
        poss_moves = Checkers.possible_moves(self.board, comp_playing=False)
        if len(poss_moves) == 0:
            if self.c_pieces > self.p_pieces:
                print(
                    "You have fewer pieces than the computer and no moves left. You have lost the game!")
            else:
                print("You have no moves left. You have lost the game!")
            exit()
        self.p_pieces = 0
        self.c_pieces = 0

        # letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
        # numbers = ["1", "2", "3", "4", "5", "6", "7", "8"]

        while True:
            current_pos = input(
                "Which piece do you want to move? ('A1'): ")
            if current_pos == "" or current_pos == "s":
                print("Game over.")
                exit()
            # cR = current_pos[0]
            # cC = current_pos[-1]
            # if cR not in letters or cC not in numbers:
            #     print(
            #         "Illegal input: please make sure to have the row capitalized and both row and column within range.")
            # elif (cR, cC) not in [move[0] for move in poss_moves]:
            #     print("Illegal input: please only enter positions where an 'x' or 'X' is located.")
            new_pos = input("Where do you want to move to? ('B2'): ")
            if new_pos == "" or new_pos == "s":
                print("Game over.")
                exit()

            cR = current_pos[0]
            cC = current_pos[-1]
            nR = new_pos[0]
            nC = new_pos[-1]

            letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
            numbers = ["1", "2", "3", "4", "5", "6", "7", "8"]
            if cR not in letters or nR not in letters or cC not in numbers or nC not in numbers:
                print(
                    "Illegal input: please make sure to have the row capitalized and both row and column within range.")
            else:
                cR = letters.index(cR)
                nR = letters.index(nR)
                cC = numbers.index(cC)
                nC = numbers.index(nC)
                move = [(cR, cC), (nR, nC)]
                if move not in poss_moves:
                    print("Oops: illegal move!")
                else:
                    Checkers.move_piece(
                        self.board, (cR, cC), (nR, nC))
                    for r in range(8):
                        for c in range(8):
                            if self.board[r][c] == " o " or self.board[r][c] == " O ":
                                self.c_pieces += 1
                            else:
                                self.p_pieces += 1
                    break

    def eval_states(self):
        t = time.time()
        curr = State(deepcopy(self.board))
        c_moves = curr.get_children(True)
        if len(c_moves) == 0:
            if self.p_pieces > self.c_pieces:
                print("You have more pieces than the computer. YOU WIN")
                exit()
            else:
                print("Computer has no available moves left. DRAW")
                exit()

        d = dict()
        for i in range(len(c_moves)):
            c = c_moves[i]
            val = Checkers.minimax(self, c.get_board(), 5, -math.inf, math.inf, False)
            d[val] = c

        if len(d.keys()) == 0:
            print("Computer has cornered itself. YOU WIN")
            exit()
        n_board = d[max(d)].get_board()
        move = d[max(d)].move
        self.board = n_board

        t1 = time.time()
        diff = t1-t

        print(
            f"Computer moved from '{str(move[0][0]), str(move[0][1])}' to '{str(move[1][0]), str(move[1][1])}'")
        print(
            f"Total time taken for computer to make move: {str(diff)} seconds")

    def minimax(self, board, n, a, b, max_player):
        if n == 0:
            return Checkers.calculate_heuristics(self, board)
        curr = State(deepcopy(self.board))
        if max_player == True:
            max_eval = -math.inf
            for c in curr.get_children(True):
                ev = Checkers.minimax(self, c.get_board(), n-1, a, b, False)
                max_eval = max(max_eval, ev)
                a = max(a, ev)
                if b <= a:
                    break
            return max_eval
        else:
            min_eval = math.inf
            for c in curr.get_children(False):
                ev = Checkers.minimax(self, c.get_board(), n-1, a, b, True)
                min_eval = min(min_eval, ev)
                b = min(b, ev)
                if b <= a:
                    break
            return min_eval

    def play(self):
        print("CHECKERS")
        print("Enter coordinates in the form: 'A1'. You are playing as 'x'.")
        print("To quit the game press enter, and to surrender the game press 's'.")
        while True:
            self.print_board()
            if self.playing:
                print("Your turn.")
                self.get_input()
            else:
                print("Computer's turn.")
                self.eval_states()
            if self.p_pieces == 0:
                self.print_board()
                print("You have run out of pieces to play. You have lost the game!")
                exit()
            elif self.c_pieces == 0:
                self.print_board()
                print(
                    "The computer has run out of pieces to play. You have won the game!")
                exit()
            self.playing = not self.playing


if __name__ == "__main__":
    checkers = Checkers()
    checkers.setup_board()
    checkers.play()
