def valid(board, current_pos, new_pos, eat, comp_playing):
        cR = current_pos[0]
        cC = current_pos[1]
        nR = new_pos[0]
        nC = new_pos[1]

        if nR > 7 or nR < 0:
            return False
        if nC > 7 or nC < 0:
            return False
        if board[cR][cC] == 0:
            return False
        if board[nR][nC] != 0:
            return False
        if comp_playing:
            if board[cR][cC].color == (255, 255, 255) :
                return False
        if not comp_playing:
            if board[cR][cC].color == (255, 0, 0):
              return False
        if eat == (-1, -1):
            return board[nR][nC] == 0
        else:
            return jump(board, current_pos, new_pos, eat)

def jump(board, current_pos, new_pos, eat=(-1, -1)):
    cR = current_pos[0]
    cC = current_pos[1]
    takeR = eat[0]
    takeC = eat[1]
    if board[takeR][takeC] == 0:
        return False
    if board[cR][cC].color == (255, 0, 0):
        if board[takeR][takeC].color == (255, 255, 255):
            return True
    if board[cR][cC] == (255, 255, 255):
        if board[takeR][takeC] == (255, 0, 0):
            return True
    return False

def possible_moves(board, comp_playing=True):
  moves = []

  for r in range(8):
      for c in range(8):
          if board[r][c] != 0:
            if comp_playing:
                if board[r][c].color == (255, 0, 0) or board[r][c].king:
                    if valid(board, (r, c), (r + 1, c + 1), (-1, -1), comp_playing):
                        moves.append([(r, c), (r + 1, c + 1)])
                    if valid(board, (r, c), (r + 1, c - 1), (-1, -1), comp_playing):
                        moves.append([(r, c), (r + 1, c - 1)])
                    if valid(board, (r, c), (r + 2, c - 2), (r+1, c-1), comp_playing):
                        moves.append([(r, c), (r + 2, c - 2)])
                    if valid(board, (r, c), (r + 2, c + 2), (r+1, c+1), comp_playing):
                        moves.append([(r, c), (r + 2, c + 2)])
                if board[r][c].king == True:
                    if valid(board, (r, c), (r - 1, c - 1), (-1, -1), comp_playing):
                        moves.append([(r, c), (r - 1, c - 1)])
                    if valid(board, (r, c), (r - 1, c + 1), (-1, -1), comp_playing):
                        moves.append([(r, c), (r - 1, c + 1)])
                    if valid(board, (r, c), (r - 2, c - 2), (r-1, c-1), comp_playing):
                        moves.append([(r, c), (r - 2, c - 2)])
                    if valid(board, (r, c), (r - 2, c + 2), (r-1, r+1), comp_playing):
                        moves.append([(r, c), (r - 2, c + 2)])
            if not comp_playing:
                if board[r][c].color == (255, 255, 255) or board[r][c].king:
                    if valid(board, (r, c), (r - 1, c - 1), (-1, -1), comp_playing):
                        moves.append([(r, c), (r - 1, c - 1)])
                    if valid(board, (r, c), (r - 1, c + 1), (-1, -1), comp_playing):
                        moves.append([(r, c), (r - 1, c + 1)])
                    if valid(board, (r, c), (r - 2, c - 2), (r-1, c-1), comp_playing):
                        moves.append([(r, c), (r - 2, c - 2)])
                    if valid(board, (r, c), (r - 2, c + 2), (r-1, c+1), comp_playing):
                        moves.append([(r, c), (r - 2, c + 2)])
                if board[r][c].king == True:
                    if valid(board, (r, c), (r + 1, c - 1), (-1, -1), comp_playing):
                        moves.append([(r, c), (r + 1, c - 1)])
                    if valid(board, (r, c), (r + 1, c + 1), (-1, -1), comp_playing):
                        moves.append([(r, c), (r + 1, c + 1)])
                    if valid(board, (r, c), (r + 2, c - 2), (r+1, c-1), comp_playing):
                        moves.append([(r, c), (r + 2, c - 2)])
                    if valid(board, (r, c), (r + 2, c + 2), (r+1, c+1), comp_playing):
                        moves.append([(r, c), (r + 2, c + 2)])

  return moves

def possible_piece_moves(board, piece, comp_playing):
    moves = []
    if piece != 0:
        r = piece.row
        c = piece.col
        if comp_playing:
            if piece.color == (255, 0, 0) or piece.king:
              if valid(board, (r, c), (r + 1, c + 1), (-1, -1), comp_playing):
                moves.append([(r, c), (r + 1, c + 1)])
              if valid(board, (r, c), (r + 1, c - 1), (-1, -1), comp_playing):
                moves.append([(r, c), (r + 1, c - 1)])
              if valid(board, (r, c), (r + 2, c - 2), (r+1, c-1), comp_playing):
                moves.append([(r, c), (r + 2, c - 2)])
              if valid(board, (r, c), (r + 2, c + 2), (r+1, c+1), comp_playing):
                moves.append([(r, c), (r + 2, c + 2)])

            if piece.king:
              if valid(board, (r, c), (r - 1, c - 1), (-1, -1), comp_playing):
                moves.append([(r, c), (r - 1, c - 1)])
              if valid(board, (r, c), (r - 1, c + 1), (-1, -1), comp_playing):
                moves.append([(r, c), (r - 1, c + 1)])
              if valid(board, (r, c), (r - 2, c - 2), (r-1, c-1), comp_playing):
                moves.append([(r, c), (r - 2, c - 2)])
              if valid(board, (r, c), (r - 2, c + 2), (r-1, r+1), comp_playing):
                moves.append([(r, c), (r - 2, c + 2)])
        if not comp_playing:
          if piece.color == (255, 255, 255) or piece.king:
              if valid(board, (r, c), (r - 1, c - 1), (-1, -1), comp_playing):
                moves.append([(r, c), (r - 1, c - 1)])
              if valid(board, (r, c), (r - 1, c + 1), (-1, -1), comp_playing):
                moves.append([(r, c), (r - 1, c + 1)])
              if valid(board, (r, c), (r - 2, c - 2), (r-1, c-1), comp_playing):
                moves.append([(r, c), (r - 2, c - 2)])
              if valid(board, (r, c), (r - 2, c + 2), (r-1, c+1), comp_playing):
                moves.append([(r, c), (r - 2, c + 2)])
          if piece.king:
              if valid(board, (r, c), (r + 1, c - 1), (-1, -1), comp_playing):
                moves.append([(r, c), (r + 1, c - 1)])
              if valid(board, (r, c), (r + 1, c + 1), (-1, -1), comp_playing):
                moves.append([(r, c), (r + 1, c + 1)])
              if valid(board, (r, c), (r + 2, c - 2), (r+1, c-1), comp_playing):
                moves.append([(r, c), (r + 2, c - 2)])
              if valid(board, (r, c), (r + 2, c + 2), (r+1, c+1), comp_playing):
                moves.append([(r, c), (r + 2, c + 2)])

    return moves