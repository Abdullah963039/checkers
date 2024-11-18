import pygame as pg
from pygame.math import Vector2

from constants import SQUARE_SIZE
from constants.colors import BLACK


white_piece = pg.transform.scale(pg.image.load("assets/white_piece.png"), (110, 110))
black_piece = pg.transform.scale(pg.image.load("assets/black_piece.png"), (110, 110))

white_king = pg.transform.scale(pg.image.load("assets/white_king.png"), (110, 110))
black_king = pg.transform.scale(pg.image.load("assets/black_king.png"), (110, 110))


class Piece:
    PADDING = 12
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.pos = Vector2(row, col)
        self.color = color
        self.king = False

        self.__piece_graphic = black_piece if color == BLACK else white_piece

    def make_king(self):
        self.king = True
        self.__piece_graphic = black_king if self.color == BLACK else white_king

    def move(self, row, col):
        self.pos = Vector2(row, col)

    def draw(self, window: pg.SurfaceType):
        x_axis = self.pos.y * SQUARE_SIZE - (
            abs(self.__piece_graphic.get_width() // 2 - SQUARE_SIZE // 2)
        )
        y_axis = self.pos.x * SQUARE_SIZE - (
            abs(self.__piece_graphic.get_height() // 2 - SQUARE_SIZE // 2)
        )

        window.blit(self.__piece_graphic, (x_axis, y_axis))

    @property
    def radius(self):
        return SQUARE_SIZE // 2 - self.PADDING

    def __deepcopy__(self, memo):
        new_piece = Piece(int(self.pos.x), int(self.pos.y), self.color)
        new_piece.king = self.king  # Copy only the necessary attributes
        return new_piece