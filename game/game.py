import pygame as pg

from constants import (
    AI_ENGINE_DEPTH,
    BOARD_HEIGHT,
    BOARD_WIDTH,
    FPS,
    PIECE_WIDTH,
    SQUARE_SIZE,
)
from constants.colors import (
    BOARD_BORDER,
    PLAYER_1,
    PLAYER_2,
    SELECTED_SQUARE_BG,
    VALID_SQUARE_BG,
    WHITE,
)

from game.board import Board
from minimax.algorithm import minimax

pg.init()
pg.display.init()


class Game:
    def __init__(self):
        self.__initialize_game()
        self.screen = pg.display.set_mode((BOARD_WIDTH, BOARD_HEIGHT), pg.RESIZABLE)
        pg.display.set_caption("My Checkers")
        self.__running = True

    def __initialize_game(self):
        self.__selected = None
        self.__board = Board()
        self.__turn = PLAYER_1
        self.__valid_moves = {}

    def start_game(self):
        clock = pg.time.Clock()

        if self.__check_winner() is not None:
            self.__end_game()

        while self.__running:
            self.screen.fill(BOARD_BORDER)
            clock.tick(FPS)
            # Event Hanlder

            if self.__turn == PLAYER_2:
                _, new_board = minimax(self.__board, AI_ENGINE_DEPTH, PLAYER_2, self)
                self.__ai_move(new_board)

            self.__handle_events()

            # Update screen
            self.__update()

        pg.quit()

    def __draw_selected_overlay(self):
        if self.__selected is None:
            return False

        # Draw the selected square if a piece is selected
        selected_row = int(self.__selected.pos.x)
        selected_col = int(self.__selected.pos.y)

        # Calculate the position of the selected square
        board_x = self.screen.get_width() // 2 - BOARD_WIDTH // 2
        board_y = self.screen.get_height() // 2 - BOARD_HEIGHT // 2

        selected_square_rect = pg.Rect(
            board_x + selected_col * SQUARE_SIZE,
            board_y + selected_row * SQUARE_SIZE,
            SQUARE_SIZE,
            SQUARE_SIZE,
        )

        # Create an overlay for the selected square
        # Create a surface with alpha
        overlay = pg.Surface((SQUARE_SIZE, SQUARE_SIZE), pg.SRCALPHA)
        # Fill with selected color and set alpha (150 for transparency)
        overlay.fill(SELECTED_SQUARE_BG + (150,))

        # Blit the overlay onto the screen first
        self.screen.blit(overlay, (selected_square_rect.x, selected_square_rect.y))

        pg.draw.circle(
            self.screen,
            WHITE,
            (
                selected_square_rect.x + 1 + SQUARE_SIZE // 2,
                selected_square_rect.y + 1 + SQUARE_SIZE // 2,
            ),
            PIECE_WIDTH // 4 + 1,
        )

        return True

    def __update(self):
        self.screen.fill(BOARD_BORDER)

        # Draw the board and valid moves
        self.__board.draw_board(self.screen)
        self.__draw_selected_overlay()
        self.draw_valid_moves(self.__valid_moves)
        pg.display.flip()

    def __handle_events(self):
        for event in pg.event.get():
            # Quit window
            if event.type == pg.QUIT:
                self.__end_game()

            if event.type == pg.VIDEORESIZE:
                new_width = max(event.w, BOARD_WIDTH)
                new_height = max(event.h, BOARD_HEIGHT)

                self.screen = pg.display.set_mode((new_width, new_height), pg.RESIZABLE)
            # Mouse click
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                row, col = self.__get_row_col_from_mouse(pos)

                self.__select(row, col)

    def __select(self, row, col):
        # User clicks on square after selecting a piece
        if self.__selected:
            valid_move = self.__move(row, col)
            if not valid_move:
                self.__selected = None
                self.__select(row, col)

        piece = self.__board.get_piece(row, col)

        if piece is None:
            self.__valid_moves = {}  # Clear valid moves
            self.__selected = None  # Deselect any selected piece
            return False

        if piece is not None and piece.color == self.__turn:
            self.__selected = piece
            self.__valid_moves = self.__board.get_valid_moves(piece)
            return True

        self.__valid_moves = {}
        self.__selected = None
        return False

    def __move(self, row, col):
        piece = self.__board.get_piece(row, col)
        if self.__selected and piece is None and (row, col) in self.__valid_moves:
            self.__board.move(self.__selected, row, col)
            skipped = self.__valid_moves[(row, col)]

            if skipped:
                self.__board.remove(skipped)

            self.__change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        # Calculate the position of the board in the window
        board_x = self.screen.get_width() // 2 - BOARD_WIDTH // 2
        board_y = self.screen.get_height() // 2 - BOARD_HEIGHT // 2

        for move in moves:
            row, col = move

            # Create a rectangle for the valid move square
            valid_move_rect = pg.Rect(
                board_x + col * SQUARE_SIZE,
                board_y + row * SQUARE_SIZE,
                SQUARE_SIZE,
                SQUARE_SIZE,
            )

            # Draw the rectangle with the specified color and transparency
            overlay = pg.Surface((SQUARE_SIZE, SQUARE_SIZE), pg.SRCALPHA)
            overlay.fill(VALID_SQUARE_BG + (180,))

            # Blit the overlay onto the screen
            self.screen.blit(overlay, (valid_move_rect.x, valid_move_rect.y))

    def __change_turn(self):
        self.__valid_moves = {}
        if self.__turn == PLAYER_1:
            self.__turn = PLAYER_2
        else:
            self.__turn = PLAYER_1

    def __check_winner(self):
        return self.__board.winner()

    def __ai_move(self, board):
        self.__board = board
        self.__change_turn()

    def __get_row_col_from_mouse(self, pos):
        x, y = pos
        # Calculate the position of the board in the window
        board_x = self.screen.get_width() // 2 - BOARD_WIDTH // 2
        board_y = self.screen.get_height() // 2 - BOARD_HEIGHT // 2

        # Adjust mouse position relative to the board
        relative_x = x - board_x
        relative_y = y - board_y

        # Calculate row and column based on the adjusted position
        row = relative_y // SQUARE_SIZE
        col = relative_x // SQUARE_SIZE

        return row, col

    def __end_game(self):
        self.__running = False
