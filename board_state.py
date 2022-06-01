import numpy as np

from bitboard_utils import get_bit
from constants import EMPTY, Color, PIECE_SYMBOLS
from board import Board

class BoardState():
    """docstring for BoardState"""
    def __init__(self):
        self.color = Color.WHITE

        self.en_passant_square = 64 # means no square

        self.is_checkmate = False
        self.is_stalemate = False

        self.castle = 0

        self.pieces_bitboard = np.zeros((2, 6), dtype=np.uint64)
        self.combined_pieces_bitboard = np.zeros(2, dtype=np.uint64)

        self.occupied_squares = EMPTY 
        
    def read_board(self, board):
        self.pieces_bitboard = board.pieces_bitboard.copy()
        # self.combined_pieces_bitboard = board.combined_pieces_bitboard.copy()
        # self.occupied_squares = board.occupied_squares.copy()

        self.color = board.color
        self.en_passant_square = board.en_passant_square
        self.castle = board.castle 

    def __str__(self):
        board = Board()
        board.pieces_bitboard = self.pieces_bitboard
        board.combined_pieces_bitboard = self.combined_pieces_bitboard
        board.occupied_squares = self.occupied_squares

        board.color = self.color
        board.en_passant_square = self.en_passant_square
        board.castle = self.castle
        return board.__str__()
