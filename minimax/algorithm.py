from copy import deepcopy

from constants.colors import PLAYER_2, PLAYER_1


def minimax(position, depth, max_player, game):
    """
    Args:
        position (Board): current board position
        depth (int): algorithm depth
        max_player (bool): if you want to maximize or minimize
        game (Game): draw and visualization
    """
    if depth == 0 or position.winner() is not None:
        return position.evaluate(), position

    if max_player:
        maxEval = float("-inf")
        best_move = None
        for move in get_all_moves(position, PLAYER_2, game):
            evaluation = minimax(move, depth - 1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move

        return maxEval, best_move

    else:
        minEval = float("inf")
        best_move = None
        for move in get_all_moves(position, PLAYER_1, game):
            evaluation = minimax(move, depth - 1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        return minEval, best_move


def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)  # This should now work without issues
            temp_piece = temp_board.get_piece(int(piece.pos.x), int(piece.pos.y))
            new_board = simulate_move(temp_piece, move, temp_board, skip)
            moves.append(new_board)

    return moves


def simulate_move(piece, move, board, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board
