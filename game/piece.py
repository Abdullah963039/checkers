import pygame as pg
from pygame.math import Vector2

from constants import PIECE_PADDING, PIECE_SIZE, SQUARE_SIZE
from constants.colors import WHITE


white_piece = pg.transform.scale(pg.image.load("assets/white_piece.png"), PIECE_SIZE)
black_piece = pg.transform.scale(pg.image.load("assets/black_piece.png"), PIECE_SIZE)

white_king = pg.transform.scale(pg.image.load("assets/white_king.png"), PIECE_SIZE)
black_king = pg.transform.scale(pg.image.load("assets/black_king.png"), PIECE_SIZE)


class Piece:
    def __init__(self, row, col, color):
        self.pos = Vector2(row, col)
        self.color = color
        self.king = False

    def make_king(self):
        self.king = True

    def move(self, row, col):
        self.pos = Vector2(row, col)

    def draw(self, window: pg.SurfaceType):
        x_axis, y_axis = self.__get_piece_graphic_position()
        graphic = self.__get_graphic()

        window.blit(graphic, (x_axis, y_axis))

    def __get_graphic(self):
        if self.king:
            return white_king if self.color == WHITE else black_king
        else:
            return white_piece if self.color == WHITE else black_piece

    @property
    def radius(self):
        return SQUARE_SIZE // 2 - PIECE_PADDING

    def __deepcopy__(self, memo):
        new_piece = Piece(int(self.pos.x), int(self.pos.y), self.color)
        new_piece.king = self.king  # Copy only the necessary attributes
        return new_piece

    def __str__(self):
        return f"({int(self.pos.x)}, {int(self.pos.y)}) {"king" if self.king else ""}"

    def __get_piece_graphic_position(self):
        graphic = self.__get_graphic()
        x_axis = self.pos.y * SQUARE_SIZE - (
            abs(graphic.get_width() // 2 - SQUARE_SIZE // 2)
        )
        y_axis = self.pos.x * SQUARE_SIZE - (
            abs(graphic.get_height() // 2 - SQUARE_SIZE // 2)
        )

        return x_axis, y_axis

    def __eq__(self, piece):
        return piece.pox.x == self.pos.x and piece.pos.y == self.pos.y