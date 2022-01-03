from enum import IntEnum
import numpy as np

EMPTY = np.uint64(0)
BIT = np.uint64(1)
UNIVERSE = np.uint64(0xFFFFFFFFFFFFFFFF)

RANKS = np.array(
    [0x00000000000000FF << 8 * i for i in range(8)],
    dtype=np.uint64)

FILES = np.array(
    [0x0101010101010101 << i for i in range(8)],
    dtype=np.uint64)

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
    A1 = np.uint64(0)
    B1 = np.uint64(1)
    C1 = np.uint64(2)
    D1 = np.uint64(3)
    E1 = np.uint64(4)
    F1 = np.uint64(5)
    G1 = np.uint64(6)
    H1 = np.uint64(7)

    A2 = np.uint64(8)
    B2 = np.uint64(9)
    C2 = np.uint64(10)
    D2 = np.uint64(11)
    E2 = np.uint64(12)
    F2 = np.uint64(13)
    G2 = np.uint64(14)
    H2 = np.uint64(15)

    A3 = np.uint64(16)
    B3 = np.uint64(17)
    C3 = np.uint64(18)
    D3 = np.uint64(19)
    E3 = np.uint64(20)
    F3 = np.uint64(21)
    G3 = np.uint64(22)
    H3 = np.uint64(23)

    A4 = np.uint64(24)
    B4 = np.uint64(25)
    C4 = np.uint64(26)
    D4 = np.uint64(27)
    E4 = np.uint64(28)
    F4 = np.uint64(29)
    G4 = np.uint64(30)
    H4 = np.uint64(31)

    A5 = np.uint64(32)
    B5 = np.uint64(33)
    C5 = np.uint64(34)
    D5 = np.uint64(35)
    E5 = np.uint64(36)
    F5 = np.uint64(37)
    G5 = np.uint64(38)
    H5 = np.uint64(39)

    A6 = np.uint64(40)
    B6 = np.uint64(41)
    C6 = np.uint64(42)
    D6 = np.uint64(43)
    E6 = np.uint64(44)
    F6 = np.uint64(45)
    G6 = np.uint64(46)
    H6 = np.uint64(47)

    A7 = np.uint64(48)
    B7 = np.uint64(49)
    C7 = np.uint64(50)
    D7 = np.uint64(51)
    E7 = np.uint64(52)
    F7 = np.uint64(53)
    G7 = np.uint64(54)
    H7 = np.uint64(55)

    A8 = np.uint64(56)
    B8 = np.uint64(57)
    C8 = np.uint64(58)
    D8 = np.uint64(59)
    E8 = np.uint64(60)
    F8 = np.uint64(61)
    G8 = np.uint64(62)
    H8 = np.uint64(63)


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

    file_A = np.uint64(0x0101010101010101)
    file_B = np.uint64(0x0202020202020202)
    file_C = np.uint64(0x0404040404040404)
    file_D = np.uint64(0x0808080808080808)
    file_E = np.uint64(0x1010101010101010)
    file_F = np.uint64(0x2020202020202020)
    file_G = np.uint64(0x4040404040404040)
    file_H = np.uint64(0x8080808080808080)


class Rank:
    x1 = [0, 1, 2, 3, 4, 5, 6, 7]
    x2 = [8, 9, 10, 11, 12, 13, 14, 15]
    x3 = [16, 17, 18, 19, 20, 21, 22, 23]
    x4 = [24, 25, 26, 27, 28, 29, 30, 31]
    x5 = [32, 33, 34, 35, 36, 37, 38, 39]
    x6 = [40, 41, 42, 43, 44, 45, 46, 47]
    x7 = [48, 49, 50, 51, 52, 53, 54, 55]
    x8 = [56, 57, 58, 59, 60, 61, 62, 63]
    
    rank_1 = np.uint64(0x00000000000000FF)
    rank_2 = np.uint64(0x000000000000FF00)
    rank_3 = np.uint64(0x0000000000FF0000)
    rank_4 = np.uint64(0x00000000FF000000)
    rank_5 = np.uint64(0x000000FF00000000)
    rank_6 = np.uint64(0x0000FF0000000000)
    rank_7 = np.uint64(0x00FF000000000000)
    rank_8 = np.uint64(0xFF00000000000000)

