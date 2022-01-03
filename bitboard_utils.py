import string
import numpy as np

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

BOARD_LENGTH = 8
BOARD_SQUARES = BOARD_LENGTH**2

def set_bit(bb, square):
	return bb | (np.ulonglong(1) << np.ulonglong(square))

def get_bit(bb, square):
	return bb & (np.ulonglong(1) << np.ulonglong(square))

def pop_bit(bb, square):
	return bb & ~(np.ulonglong(1) << np.ulonglong(square))

def count_bits(bb):
	count = 0
	while bb:
		count += 1
		bb &= bb - np.ulonglong(1)
	return int(count)

def get_lsb1_index(bb):
	if bb:
		return count_bits((bb & -bb) - np.ulonglong(1))
	else:
		return -1


def print_bb(bb):
    print("\n")
    for rank in range(8):
        r = ""
        for file in range(8):
            sq = rank * 8 + file
            r += f" {'1' if get_bit(bb, sq) else '·'} "
        print(8 - rank, r)
    print("   A  B  C  D  E  F  G  H")

    print("Bitboard:", bb)