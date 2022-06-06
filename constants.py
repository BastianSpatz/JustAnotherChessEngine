from enum import IntEnum
import numpy as np


BOARD_LENGTH = 8
BOARD_SQUARES = BOARD_LENGTH**2
(
    a8,    b8,    c8,    d8,    e8,    f8,    g8,    h8,
    a7,    b7,    c7,    d7,    e7,    f7,    g7,    h7,
    a6,    b6,    c6,    d6,    e6,    f6,    g6,    h6,
    a5,    b5,    c5,    d5,    e5,    f5,    g5,    h5,
    a4,    b4,    c4,    d4,    e4,    f4,    g4,    h4,
    a3,    b3,    c3,    d3,    e3,    f3,    g3,    h3,
    a2,    b2,    c2,    d2,    e2,    f2,    g2,    h2,
    a1,    b1,    c1,    d1,    e1,    f1,    g1,    h1,
    no_sq,
) = np.arange(BOARD_SQUARES + 1, dtype=np.uint8)

pawn, knight, bishop, rook, queen, king = range(6)

Pieces = [pawn, knight, bishop, rook, queen, king]

def piece_from_symbol(symbol: str):
    piece = None
    
    if symbol.lower() == "p":
        piece = pawn
    elif symbol.lower() == "n":
        piece = knight
    elif symbol.lower() == "b":
        piece = bishop
    elif symbol.lower() == "r":
        piece = rook
    elif symbol.lower() == "q":
        piece = queen
    elif symbol.lower() == "k":
        piece = king
    else:
        print("Symbol not found..")
        return
    if symbol.isupper():
        return piece, white
    else:
        return piece, black

white, black, both = np.arange(3, dtype=np.uint8)

EMPTY = np.ulonglong(0)
BIT = np.ulonglong(1)
UNIVERSE = np.ulonglong(0xFFFFFFFFFFFFFFFF)

STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
tricky_position = "r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq - 0 1 "
killer_position = "rnbqkb1r/pp1p1pPp/8/2p1pP2/1P1P4/3P3P/P1P1P3/RNBQKBNR w KQkq e6 0 1"
cmk_position = "r2q1rk1/ppp2ppp/2n1bn2/2b1p3/3pP3/3P1NPP/PPP1NPB1/R1BQ1RK1 b - - 0 9 "


wk, wq, bk, bq = (2 ** i for i in range(4))


PIECE_SYMBOLS = ["P", "N", "B", "R", "Q", "K", "p", "n", "b", "r", "q", "k"]

UNICODE_PIECE_SYMBOLS = {
    "r": "♖", "R": "♜",
    "n": "♘", "N": "♞",
    "b": "♗", "B": "♝",
    "q": "♕", "Q": "♛",
    "k": "♔", "K": "♚",
    "p": "♙", "P": "♟",
}



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

castling_rights = [
     7, 15, 15, 15,  3, 15, 15, 11,
    15, 15, 15, 15, 15, 15, 15, 15,
    15, 15, 15, 15, 15, 15, 15, 15,
    15, 15, 15, 15, 15, 15, 15, 15,
    15, 15, 15, 15, 15, 15, 15, 15,
    15, 15, 15, 15, 15, 15, 15, 15,
    15, 15, 15, 15, 15, 15, 15, 15,
    13, 15, 15, 15, 12, 15, 15, 14
]


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
    x1 = [56, 57, 58, 59, 60, 61, 62, 63]
    x2 = [48, 49, 50, 51, 52, 53, 54, 55]
    x3 = [40, 41, 42, 43, 44, 45, 46, 47]
    x4 = [32, 33, 34, 35, 36, 37, 38, 39]
    x5 = [24, 25, 26, 27, 28, 29, 30, 31]
    x6 = [16, 17, 18, 19, 20, 21, 22, 23]
    x7 = [8, 9, 10, 11, 12, 13, 14, 15]
    x8 = [0, 1, 2, 3, 4, 5, 6, 7]
    
    rank_1 = np.ulonglong(0xFF00000000000000)
    rank_2 = np.ulonglong(0x00FF000000000000)
    rank_3 = np.ulonglong(0x0000FF0000000000)
    rank_4 = np.ulonglong(0x000000FF00000000)
    rank_5 = np.ulonglong(0x00000000FF000000)
    rank_6 = np.ulonglong(0x0000000000FF0000)
    rank_7 = np.ulonglong(0x000000000000FF00)
    rank_8 = np.ulonglong(0x00000000000000FF)

material_score = [100,      # white pawn score
                300,      # white knight scrore
                350,      # white bishop score
                500,      # white rook score
               1000,      # white queen score
              10000,      # white king score
               -100,      # black pawn score
               -300,      # black knight scrore
               -350,      # black bishop score
               -500,      # black rook score
              -1000,      # black queen score
             -10000]     # black king score

# pawn positional score
pawn_score = [90,  90,  90,  90,  90,  90,  90,  90,
            30,  30,  30,  40,  40,  30,  30,  30,
            20,  20,  20,  30,  30,  30,  20,  20,
            10,  10,  10,  20,  20,  10,  10,  10,
             5,   5,  10,  20,  20,   5,   5,   5,
             0,   0,   0,   5,   5,   0,   0,   0,
             0,   0,   0, -10, -10,   0,   0,   0,
             0,   0,   0,   0,   0,   0,   0,   0]

# knight positional score
knight_score =[-5,   0,   0,   0,   0,   0,   0,  -5,
            -5,   0,   0,  10,  10,   0,   0,  -5,
            -5,   5,  20,  20,  20,  20,   5,  -5,
            -5,  10,  20,  30,  30,  20,  10,  -5,
            -5,  10,  20,  30,  30,  20,  10,  -5,
            -5,   5,  20,  10,  10,  20,   5,  -5,
            -5,   0,   0,   0,   0,   0,   0,  -5,
            -5, -10,   0,   0,   0,   0, -10,  -5
        ]

# bishop positional score
bishop_score =[0,   0,   0,   0,   0,   0,   0,   0,
             0,   0,   0,   0,   0,   0,   0,   0,
             0,   0,   0,  10,  10,   0,   0,   0,
             0,   0,  10,  20,  20,  10,   0,   0,
             0,   0,  10,  20,  20,  10,   0,   0,
             0,  10,   0,   0,   0,   0,  10,   0,
             0,  30,   0,   0,   0,   0,  30,   0,
             0,   0, -10,   0,   0, -10,   0,   0

]

# rook positional score
rook_score =[50,  50,  50,  50,  50,  50,  50,  50,
            50,  50,  50,  50,  50,  50,  50,  50,
             0,   0,  10,  20,  20,  10,   0,   0,
             0,   0,  10,  20,  20,  10,   0,   0,
             0,   0,  10,  20,  20,  10,   0,   0,
             0,   0,  10,  20,  20,  10,   0,   0,
             0,   0,  10,  20,  20,  10,   0,   0,
             0,   0,   0,  20,  20,   0,   0,   0

]

# king positional score
king_score =[0,   0,   0,   0,   0,   0,   0,   0,
             0,   0,   5,   5,   5,   5,   0,   0,
             0,   5,   5,  10,  10,   5,   5,   0,
             0,   5,  10,  20,  20,  10,   5,   0,
             0,   5,  10,  20,  20,  10,   5,   0,
             0,   0,   5,  10,  10,   5,   0,   0,
             0,   5,   5,  -5,  -5,   0,   5,   0,
             0,   0,   5,   0, -15,   0,  10,   0
        ]

# mirror positional score tables for opposite side
mirror_score =[a1, b1, c1, d1, e1, f1, g1, h1,
            a2, b2, c2, d2, e2, f2, g2, h2,
            a3, b3, c3, d3, e3, f3, g3, h3,
            a4, b4, c4, d4, e4, f4, g4, h4,
            a5, b5, c5, d5, e5, f5, g5, h5,
            a6, b6, c6, d6, e6, f6, g6, h6,
            a7, b7, c7, d7, e7, f7, g7, h7,
            a8, b8, c8, d8, e8, f8, g8, h8
        ]

