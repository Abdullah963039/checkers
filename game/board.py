import pygame as pg

from constants import COLS_NUM, ROWS_NUM, BOARD_HEIGHT, BOARD_WIDTH, SQUARE_SIZE
from constants.colors import DARK_SQUARE, LIGHT_SQUARE, PLAYER_1, PLAYER_2
from game.piece import Piece


class Board:
    def __init__(self):
        self.board = []
        self.p1_left = self.p2_left = 12
        self.p1_kings = self.p2_kings = 0
        self.__create_board()

    def draw_board(self, window: pg.Surface):
        board_surface = self.__draw_squares()
        for row in range(ROWS_NUM):
            for col in range(COLS_NUM):
                piece = self.board[row][col]
                if piece is not None:
                    piece.draw(board_surface)

        window.blit(
            board_surface,
            (
                window.get_width() // 2 - board_surface.get_width() // 2,
                window.get_height() // 2 - board_surface.get_height() // 2,
            ),
        )

    def __draw_squares(self):
        surface = pg.Surface((BOARD_WIDTH, BOARD_HEIGHT))

        for row in range(ROWS_NUM):
            if row % 2 == 0:
                for col in range(COLS_NUM):
                    square_rect = pg.Rect(
                        row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE
                    )
                    if col % 2 == 0:
                        pg.draw.rect(surface, LIGHT_SQUARE, square_rect)
                    else:
                        pg.draw.rect(surface, DARK_SQUARE, square_rect)

            else:
                for col in range(COLS_NUM):
                    square_rect = pg.Rect(
                        row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE
                    )
                    if col % 2 != 0:
                        pg.draw.rect(surface, LIGHT_SQUARE, square_rect)
                    else:
                        pg.draw.rect(surface, DARK_SQUARE, square_rect)
        return surface

    def __create_board(self):
        for row in range(ROWS_NUM):
            self.board.append([])
            for col in range(COLS_NUM):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, PLAYER_2))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, PLAYER_1))
                    else:
                        self.board[row].append(None)
                else:
                    self.board[row].append(None)

    def get_piece(self, row, col):
        return self.board[row][col]

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece is not None and piece.color == color:
                    pieces.append(piece)
        return pieces

    def evaluate(self):
        return self.p2_left - self.p1_left + (self.p2_kings * 0.5 - self.p1_kings * 0.5)

    def move(self, piece: Piece, row, col):
        self.board[int(piece.pos.x)][int(piece.pos.y)], self.board[row][col] = (
            self.board[row][col],
            self.board[int(piece.pos.x)][int(piece.pos.y)],
        )
        piece.move(row, col)

        if row == ROWS_NUM - 1 or row == 0:
            piece.make_king()
            if piece.color == PLAYER_1:
                self.p1_kings += 1
            else:
                self.p2_kings += 1

    def get_valid_moves(self, piece: Piece):
        moves = {}
        left = int(piece.pos.y - 1)
        right = int(piece.pos.y + 1)
        row = int(piece.pos.x)

        if piece.color == PLAYER_1 or piece.king:
            moves.update(
                self.__traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left)
            )
            moves.update(
                self.__traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right)
            )

        if piece.color == PLAYER_2 or piece.king:
            moves.update(
                self.__traverse_left(
                    row + 1, min(row + 3, ROWS_NUM), 1, piece.color, left
                )
            )
            moves.update(
                self.__traverse_right(
                    row + 1, min(row + 3, ROWS_NUM), 1, piece.color, right
                )
            )

        return moves

    def get_valid_player_moves(self, color):
        total_valid_moves = 0

        for piece in self.get_all_pieces(color):
            if piece is None:
                return 0
            valid_moves = self.get_valid_moves(piece)
            total_valid_moves += len(valid_moves)

        return total_valid_moves
    
    def remove(self, pieces):
        for piece in pieces:
            #TODO: piece.capture()
            self.board[int(piece.pos.x)][int(piece.pos.y)] = None

        if piece is not None:
            if piece.color == PLAYER_1:
                self.p1_left -= 1
            else:
                self.p2_left -= 1

    def __traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break

            current = self.board[r][left]

            if current is None:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS_NUM)

                    moves.update(
                        self.__traverse_left(
                            r + step, row, step, color, left - 1, skipped=last
                        )
                    )
                    moves.update(
                        self.__traverse_right(
                            r + step, row, step, color, left + 1, skipped=last
                        )
                    )
                break

            elif current.color == color:
                break

            else:
                last = [current]

            left -= 1

        return moves

    def __traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS_NUM:
                break

            current = self.board[r][right]
            if current is None:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped
                else:
                    moves[(r, right)] = last

                if last:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, ROWS_NUM)

                    moves.update(
                        self.__traverse_left(
                            r + step, row, step, color, right - 1, skipped=last
                        )
                    )
                    moves.update(
                        self.__traverse_right(
                            r + step, row, step, color, right + 1, skipped=last
                        )
                    )
                break

            elif current.color == color:
                break

            else:
                last = [current]

            right += 1

        return moves

    def winner(self):
        if self.p1_left <= 0 or self.get_valid_player_moves(PLAYER_1) == 0:
            return PLAYER_2
        elif self.p2_left <= 0 or self.get_valid_player_moves(PLAYER_2) == 0:
            return PLAYER_1
        else:
            return None

