from enum import IntEnum
import numpy as np


BOARD_LENGTH = 8
BOARD_SQUARES = BOARD_LENGTH**2

EMPTY = np.ulonglong(0)
BIT = np.ulonglong(1)
UNIVERSE = np.ulonglong(0xFFFFFFFFFFFFFFFF)

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

SQUARES = [
    A1, B1, C1, D1, E1, F1, G1, H1,
    A2, B2, C2, D2, E2, F2, G2, H2,
    A3, B3, C3, D3, E3, F3, G3, H3,
    A4, B4, C4, D4, E4, F4, G4, H4,
    A5, B5, C5, D5, E5, F5, G5, H5,
    A6, B6, C6, D6, E6, F6, G6, H6,
    A7, B7, C7, D7, E7, F7, G7, H7,
    A8, B8, C8, D8, E8, F8, G8, H8,
] = range(BOARD_SQUARES)

BB_SQUARES = [
    BB_A1, BB_B1, BB_C1, BB_D1, BB_E1, BB_F1, BB_G1, BB_H1,
    BB_A2, BB_B2, BB_C2, BB_D2, BB_E2, BB_F2, BB_G2, BB_H2,
    BB_A3, BB_B3, BB_C3, BB_D3, BB_E3, BB_F3, BB_G3, BB_H3,
    BB_A4, BB_B4, BB_C4, BB_D4, BB_E4, BB_F4, BB_G4, BB_H4,
    BB_A5, BB_B5, BB_C5, BB_D5, BB_E5, BB_F5, BB_G5, BB_H5,
    BB_A6, BB_B6, BB_C6, BB_D6, BB_E6, BB_F6, BB_G6, BB_H6,
    BB_A7, BB_B7, BB_C7, BB_D7, BB_E7, BB_F7, BB_G7, BB_H7,
    BB_A8, BB_B8, BB_C8, BB_D8, BB_E8, BB_F8, BB_G8, BB_H8,
] = [1 << sq for sq in SQUARES]

def square_mirror(square):
    """Mirrors the square vertically."""
    return square ^ 0x38
    
SQUARES_180 = [square_mirror(sq) for sq in SQUARES]

RANKS = np.array(
    [0x00000000000000FF << 8 * i for i in range(8)],
    dtype=np.ulonglong)

FILES = np.array(
    [0x0101010101010101 << i for i in range(8)],
    dtype=np.ulonglong)

class Color(IntEnum):
    WHITE=0
    BLACK=1

    def __str__(self):
        if self == Color.WHITE:
            return "w"
        else:
            return "b"

    def __invert__(self):
        if self == Color.WHITE:
            return Color.BLACK
        else:
            return Color.WHITE


class Piece(IntEnum):
    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5

    def __str__(self):
        if self == Piece.PAWN:
            return "PAWN"
        elif self == Piece.KNIGHT:
            return "KNIGHT"
        elif self == Piece.BISHOP:
            return "BISHOP"
        elif self == Piece.ROOK:
            return "ROOK"
        elif self == Piece.QUEEN:
            return "QUEEN"
        else:
            return "KING"

    def __from_symbol__(symbol: str):
        piece = None
        
        if symbol.lower() == "p":
            piece = Piece.PAWN
        elif symbol.lower() == "n":
            piece = Piece.KNIGHT
        elif symbol.lower() == "b":
            piece = Piece.BISHOP
        elif symbol.lower() == "r":
            piece = Piece.ROOK
        elif symbol.lower() == "q":
            piece = Piece.QUEEN
        elif symbol.lower() == "k":
            piece = Piece.KING
        else:
            print("Symbol not found..")
            return

        if symbol.isupper():
            return piece, Color.WHITE
        else:
            return piece, Color.BLACK

    def __to_symbol__(self, color):
        if self == Piece.PAWN:
            if color == Color.WHITE:
                return "P"
            else:
                return "p"
        elif self == Piece.KNIGHT:
            if color == Color.WHITE:
                return "N"
            else:
                return "n"
        elif self == Piece.BISHOP:
            if color == Color.WHITE:
                return "B"
            else:
                return "b"
        elif self == Piece.ROOK:
            if color == Color.WHITE:
                return "R"
            else:
                return "r"
        elif self == Piece.QUEEN:
            if color == Color.WHITE:
                return "Q"
            else:
                return "q"
        else:
            if color == Color.WHITE:
                return "K"
            else:
                return "k"


PIECE_SYMBOLS = ["P", "R", "N", "B", "Q", "K", "p", "r", "n", "b", "q", "k"]

UNICODE_PIECE_SYMBOLS = {
    "R": "♖", "r": "♜",
    "N": "♘", "n": "♞",
    "B": "♗", "b": "♝",
    "Q": "♕", "q": "♛",
    "K": "♔", "k": "♚",
    "P": "♙", "p": "♟",
}

class Square:
    A1 = np.ulonglong(0)
    B1 = np.ulonglong(1)
    C1 = np.ulonglong(2)
    D1 = np.ulonglong(3)
    E1 = np.ulonglong(4)
    F1 = np.ulonglong(5)
    G1 = np.ulonglong(6)
    H1 = np.ulonglong(7)

    A2 = np.ulonglong(8)
    B2 = np.ulonglong(9)
    C2 = np.ulonglong(10)
    D2 = np.ulonglong(11)
    E2 = np.ulonglong(12)
    F2 = np.ulonglong(13)
    G2 = np.ulonglong(14)
    H2 = np.ulonglong(15)

    A3 = np.ulonglong(16)
    B3 = np.ulonglong(17)
    C3 = np.ulonglong(18)
    D3 = np.ulonglong(19)
    E3 = np.ulonglong(20)
    F3 = np.ulonglong(21)
    G3 = np.ulonglong(22)
    H3 = np.ulonglong(23)

    A4 = np.ulonglong(24)
    B4 = np.ulonglong(25)
    C4 = np.ulonglong(26)
    D4 = np.ulonglong(27)
    E4 = np.ulonglong(28)
    F4 = np.ulonglong(29)
    G4 = np.ulonglong(30)
    H4 = np.ulonglong(31)

    A5 = np.ulonglong(32)
    B5 = np.ulonglong(33)
    C5 = np.ulonglong(34)
    D5 = np.ulonglong(35)
    E5 = np.ulonglong(36)
    F5 = np.ulonglong(37)
    G5 = np.ulonglong(38)
    H5 = np.ulonglong(39)

    A6 = np.ulonglong(40)
    B6 = np.ulonglong(41)
    C6 = np.ulonglong(42)
    D6 = np.ulonglong(43)
    E6 = np.ulonglong(44)
    F6 = np.ulonglong(45)
    G6 = np.ulonglong(46)
    H6 = np.ulonglong(47)

    A7 = np.ulonglong(48)
    B7 = np.ulonglong(49)
    C7 = np.ulonglong(50)
    D7 = np.ulonglong(51)
    E7 = np.ulonglong(52)
    F7 = np.ulonglong(53)
    G7 = np.ulonglong(54)
    H7 = np.ulonglong(55)

    A8 = np.ulonglong(56)
    B8 = np.ulonglong(57)
    C8 = np.ulonglong(58)
    D8 = np.ulonglong(59)
    E8 = np.ulonglong(60)
    F8 = np.ulonglong(61)
    G8 = np.ulonglong(62)
    H8 = np.ulonglong(63)


square_to_coordinates = [
    "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8",
    "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7",
    "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6",
    "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5",
    "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4",
    "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3",
    "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2",
    "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"
    ]

"""
big-endian rank-file mapping:
 0  1  2  3  4  5  6  7         A8 B8 C8 D8 E8 F8 G8 H8
 8  9 10 11 12 13 14 15         A7 B7 C7 D7 E7 F7 G7 H7
16 17 18 19 20 21 22 23         A6 B6 C6 D6 E6 F6 G6 H6
24 25 26 27 28 29 30 31    =    A5 B5 C5 D5 E5 F5 G5 H5
32 33 34 35 36 37 38 39         A4 B4 C4 D4 E4 F4 G4 H4
40 41 42 43 44 45 46 47         A3 B3 C3 D3 E3 F3 G3 H3
48 49 50 51 52 53 54 55         A2 B2 C2 D2 E2 F2 G2 H2
56 57 58 59 60 61 62 63         A1 B1 C1 D1 E1 F1 G1 H1
"""

algebraic_square_map = {
    'a8': 0, 'b8': 1, 'c8': 2, 'd8': 3,'e8': 4,'f8': 5,'g8': 6,'h8': 7,
    'a7': 8,'b7': 9,'c7': 10,'d7': 11,'e7': 12,'f7': 13,'g7': 14,'h7': 15,
    'a6': 16,'b6': 17,'c6': 18,'d6': 19,'e6': 20,'f6': 21,'g6': 22,'h6': 23,
    'a5': 24,'b5': 25,'c5': 26,'d5': 27,'e5': 28,'f5': 29,'g5': 30,'h5': 31,
    'a4': 32,'b4': 33,'c4': 34,'d4': 35,'e4': 36,'f4': 37,'g4': 38,'h4': 39,
    'a3': 40,'b3': 41,'c3': 42,'d3': 43,'e3': 44,'f3': 45,'g3': 46,'h3': 47,
    'a2': 48,'b2': 49,'c2': 50,'d2': 51,'e2': 52,'f2': 53,'g2': 54,'h2': 55,
    'a1': 56,'b1': 57,'c1': 58,'d1': 59,'e1': 60,'f1': 61,'g1': 62,'h1': 63
}


class File:
    A = [0, 8, 16, 24, 32, 40, 48, 56]
    B = [1, 9, 17, 25, 33, 41, 49, 57]
    C = [2, 10, 18, 26, 34, 42, 50, 58]
    D = [3, 11, 19, 27, 35, 43, 51, 59]
    E = [4, 12, 20, 28, 36, 44, 52, 60]
    F = [5, 13, 21, 29, 37, 45, 53, 61]
    G = [6, 14, 22, 30, 38, 46, 54, 62]
    H = [7, 15, 23, 31, 39, 47, 55, 63]

    file_A = np.ulonglong(0x0101010101010101)
    file_B = np.ulonglong(0x0202020202020202)
    file_C = np.ulonglong(0x0404040404040404)
    file_D = np.ulonglong(0x0808080808080808)
    file_E = np.ulonglong(0x1010101010101010)
    file_F = np.ulonglong(0x2020202020202020)
    file_G = np.ulonglong(0x4040404040404040)
    file_H = np.ulonglong(0x8080808080808080)


class Rank:
    x1 = [0, 1, 2, 3, 4, 5, 6, 7]
    x2 = [8, 9, 10, 11, 12, 13, 14, 15]
    x3 = [16, 17, 18, 19, 20, 21, 22, 23]
    x4 = [24, 25, 26, 27, 28, 29, 30, 31]
    x5 = [32, 33, 34, 35, 36, 37, 38, 39]
    x6 = [40, 41, 42, 43, 44, 45, 46, 47]
    x7 = [48, 49, 50, 51, 52, 53, 54, 55]
    x8 = [56, 57, 58, 59, 60, 61, 62, 63]
    
    rank_1 = np.ulonglong(0x00000000000000FF)
    rank_2 = np.ulonglong(0x000000000000FF00)
    rank_3 = np.ulonglong(0x0000000000FF0000)
    rank_4 = np.ulonglong(0x00000000FF000000)
    rank_5 = np.ulonglong(0x000000FF00000000)
    rank_6 = np.ulonglong(0x0000FF0000000000)
    rank_7 = np.ulonglong(0x00FF000000000000)
    rank_8 = np.ulonglong(0xFF00000000000000)

