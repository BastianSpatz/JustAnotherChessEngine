import string
import numpy as np


def set_bit(bitboard: np.ulonglong, square: int):
	return bitboard | (np.ulonglong(1) << np.ulonglong(square))

def get_bit(bitboard: np.ulonglong, square: int):
	return bitboard & (np.ulonglong(1) << np.ulonglong(square))

def pop_bit(bitboard: np.ulonglong, square: int):
	return bitboard & ~(np.ulonglong(1) << np.ulonglong(square))

def count_bits(bitboard: np.ulonglong):
	count = 0
	while bitboard:
		count += 1
		bitboard &= bitboard - np.ulonglong(1)
	return count

# get least significant bit
def get_lsb1_index(bitboard: np.ulonglong):
	return count_bits((bitboard & -bitboard) - np.ulonglong(1))

# debug print function
def print_bitboard(bitboard: np.ulonglong):
    print("\n")
    for rank in range(8):
        r = ""
        for file in range(8):
            sq = rank * 8 + file
            r += f" {'1' if get_bit(bitboard, sq) else '·'} "
        print(8 - rank, r)
    print("   A  B  C  D  E  F  G  H")

    print("Bitboard:", bitboard)