from bitboard_utils import *
from constants import *


#################################################
# PIECE MASKS 									#
#################################################

def mask_pawn_attacks(square: int, color: int):
	bitboard = set_bit(EMPTY, square)

	if color == white:
		west_attacks = (bitboard >> np.ulonglong(9)) & ~File.file_H
		east_attacks = (bitboard >> np.ulonglong(7)) & ~File.file_A
	else:
		east_attacks = (bitboard << np.ulonglong(9)) & ~File.file_A
		west_attacks = (bitboard << np.ulonglong(7)) & ~File.file_H
	return east_attacks | west_attacks

def mask_knight_attacks(square: int):
	bitboard = EMPTY
	for bit in [17, -17, 10, -10, 15, -15, 6, -6]:
		bitboard |= set_bit(bitboard, square + bit)
		if square in (File.A + File.B):
			bitboard &= ~(File.file_H | File.file_G)
		if square in (File.G + File.H):
			bitboard &= ~(File.file_A | File.file_B)
	return bitboard 

def mask_king_attacks(square: int):
	bitboard = EMPTY
	for bit in [1, -1, 7, -7, 8, -8, 9, -9]:
		bitboard = set_bit(bitboard, square + bit)

		if square in File.A:
			bitboard &= ~File.file_H
		if square in File.H:
			bitboard &= ~File.file_A
	return bitboard

def mask_bishop_attacks(square: int):
	attacks = EMPTY
	tr = square // 8
	tf = square % 8

	for direction in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
		for i in range(1, 7):
			r = tr + direction[0] * i
			f = tf + direction[1] * i
			if not 0 < r < 7 or not 0 < f < 7:
				break
			attacks |= (np.ulonglong(1) << np.ulonglong(r * 8 + f))

	return attacks

def mask_rook_attacks(square: int):
	attacks = EMPTY
	tr = square // 8
	tf = square % 8

	for direction in (-1, 1):
		for i in range(1, 7):
			r = tr + direction * i
			if not 0 < r < 7:
				break
			attacks |= np.ulonglong(1) << np.ulonglong(r * 8 + tf)

		for i in range(1, 7):
			f = tf + direction * i
			if not 0 < f < 7:
				break
			attacks |= np.ulonglong(1) << np.ulonglong(tr * 8 + f)

	return attacks


#################################################
# SLIDER PIECES BITBOARD WITH OCCUPANCY 		#
#################################################

def bishop_attacks_with_occupancy(square: int, occupancy: np.ulonglong):
	attacks = EMPTY
	tr = square // 8
	tf = square % 8

	for direction in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
		for reach in range(1, 8):
			r = tr + direction[0] * reach
			f = tf + direction[1] * reach
			if not 0 <= r <= 7 or not 0 <= f <= 7:
				break
			attacked_bit = BIT << np.ulonglong(r * 8 + f)
			attacks |= attacked_bit
			if attacked_bit & occupancy:
				break

	return attacks


def rook_attacks_with_occupancy(square: int, occupancy: np.ulonglong):
	attacks = EMPTY
	tr = square // 8
	tf = square % 8

	for direction in (1, -1):
		for i in range(1, 8):
			r = tr + direction * i
			if not 0 <= r <= 7:
				break
			attacked_bit = BIT << np.ulonglong(r * 8 + tf)
			attacks |= attacked_bit
			if attacked_bit & occupancy:
				break

		for i in range(1, 8):
			f = tf + direction * i
			if not 0 <= f <= 7:
				break
			attacked_bit = BIT << np.ulonglong(tr * 8 + f)
			attacks |= attacked_bit
			if attacked_bit & occupancy:
				break

	return attacks

#################################################
# THE RELEVANT BITS FOR SLIDER PIECES	 		#
#################################################

bishop_relevant_bits = np.array([
	6, 5, 5, 5, 5, 5, 5, 6, 
	5, 5, 5, 5, 5, 5, 5, 5, 
	5, 5, 7, 7, 7, 7, 5, 5, 
	5, 5, 7, 9, 9, 7, 5, 5, 
	5, 5, 7, 9, 9, 7, 5, 5, 
	5, 5, 7, 7, 7, 7, 5, 5, 
	5, 5, 5, 5, 5, 5, 5, 5, 
	6, 5, 5, 5, 5, 5, 5, 6
], dtype=int)

rook_relevant_bits = np.array([
	12, 11, 11, 11, 11, 11, 11, 12, 
	11, 10, 10, 10, 10, 10, 10, 11, 
	11, 10, 10, 10, 10, 10, 10, 11, 
	11, 10, 10, 10, 10, 10, 10, 11, 
	11, 10, 10, 10, 10, 10, 10, 11, 
	11, 10, 10, 10, 10, 10, 10, 11, 
	11, 10, 10, 10, 10, 10, 10, 11, 
	12, 11, 11, 11, 11, 11, 11, 12
], dtype=int)


def bishop_attacks_with_occupancy(square: int, block: np.ulonglong):
	attacks = EMPTY
	tr = square // 8
	tf = square % 8

	for direction in ((1, 1), (-1, 1), (1, -1), (-1, -1)):
		for reach in range(1, 8):
			r = tr + direction[0] * reach
			f = tf + direction[1] * reach
			if not 0 <= r <= 7 or not 0 <= f <= 7:
				break
			attacked_bit = np.ulonglong(1) << np.ulonglong(r * 8 + f)
			attacks |= attacked_bit
			if attacked_bit & block:
				break

	return attacks

def rook_attacks_with_occupancy(square: int, block: np.ulonglong):
	attacks = EMPTY
	tr = square // 8
	tf = square % 8

	for direction in (1, -1):
		for i in range(1, 8):
			r = tr + direction * i
			if not 0 <= r <= 7:
				break
			attacked_bit = np.ulonglong(1) << np.ulonglong(r * 8 + tf)
			attacks |= attacked_bit
			if attacked_bit & block:
				break

		for i in range(1, 8):
			f = tf + direction * i
			if not 0 <= f <= 7:
				break
			attacked_bit = np.ulonglong(1) << np.ulonglong(tr * 8 + f)
			attacks |= attacked_bit
			if attacked_bit & block:
				break

	return attacks

def set_occupancy(index: int, bits_in_mask: int, attack_mask: np.ulonglong):
	occupancy = EMPTY

	for count in range(bits_in_mask):

		square = get_lsb1_index(attack_mask)

		attack_mask = pop_bit(attack_mask, square)

		if index & (1 << count):
			occupancy |= np.ulonglong(1) << np.ulonglong(square)

	return occupancy

rook_magic_numbers = np.array([0x8a80104000800020,  0x140002000100040,  0x2801880a0017001,
							   0x100081001000420,   0x200020010080420,  0x3001c0002010008,
							   0x8480008002000100,  0x2080088004402900, 0x800098204000,
							   0x2024401000200040,  0x100802000801000,  0x120800800801000,
							   0x208808088000400,   0x2802200800400,    0x2200800100020080,
							   0x801000060821100,   0x80044006422000,   0x100808020004000,
							   0x12108a0010204200,  0x140848010000802,  0x481828014002800,
							   0x8094004002004100,  0x4010040010010802, 0x20008806104,
							   0x100400080208000,   0x2040002120081000, 0x21200680100081,
							   0x20100080080080,    0x2000a00200410,    0x20080800400,
							   0x80088400100102,    0x80004600042881,   0x4040008040800020,
							   0x440003000200801,   0x4200011004500,    0x188020010100100,
							   0x14800401802800,    0x2080040080800200, 0x124080204001001,
							   0x200046502000484,   0x480400080088020,  0x1000422010034000,
							   0x30200100110040,    0x100021010009,     0x2002080100110004,
							   0x202008004008002,   0x20020004010100,   0x2048440040820001,
							   0x101002200408200,   0x40802000401080,   0x4008142004410100,
							   0x2060820c0120200,   0x1001004080100,    0x20c020080040080,
							   0x2935610830022400,  0x44440041009200,   0x280001040802101,
							   0x2100190040002085,  0x80c0084100102001, 0x4024081001000421,
							   0x20030a0244872,     0x12001008414402,   0x2006104900a0804,
							   0x1004081002402], dtype=np.ulonglong)

bishop_magic_numbers = np.array([0x40040844404084,      0x2004208a004208,       0x10190041080202,
								 0x108060845042010,     0x581104180800210,      0x2112080446200010,
								 0x1080820820060210,    0x3c0808410220200,      0x4050404440404,
								 0x21001420088,         0x24d0080801082102,     0x1020a0a020400,
								 0x40308200402,         0x4011002100800,        0x401484104104005,
								 0x801010402020200,     0x400210c3880100,       0x404022024108200,
								 0x810018200204102,     0x4002801a02003,        0x85040820080400,
								 0x810102c808880400,    0xe900410884800,        0x8002020480840102,
								 0x220200865090201,     0x2010100a02021202,     0x152048408022401,
								 0x20080002081110,      0x4001001021004000,     0x800040400a011002,
								 0xe4004081011002,      0x1c004001012080,       0x8004200962a00220,
								 0x8422100208500202,    0x2000402200300c08,     0x8646020080080080,
								 0x80020a0200100808,    0x2010004880111000,     0x623000a080011400,
								 0x42008c0340209202,    0x209188240001000,      0x400408a884001800,
								 0x110400a6080400,      0x1840060a44020800,     0x90080104000041,
								 0x201011000808101,     0x1a2208080504f080,     0x8012020600211212,
								 0x500861011240000,     0x180806108200800,      0x4000020e01040044,
								 0x300000261044000a,    0x802241102020002,      0x20906061210001,
								 0x5a84841004010310,    0x4010801011c04,        0xa010109502200,
								 0x4a02012000,          0x500201010098b028,     0x8040002811040900,
								 0x28000010020204,      0x6000020202d0240,      0x8918844842082200,
								 0x401001102902002], dtype=np.ulonglong)

rook_masks = np.fromiter((mask_rook_attacks(square) for square in range(64)), dtype=np.ulonglong)

bishop_masks = np.fromiter((mask_bishop_attacks(square) for square in range(64)), dtype=np.ulonglong)

def init_sliders(attacks: np.ulonglong, is_bishop: bool):
	"""initialize bishop and rook attack tables with their magic numbers"""

	for sq in range(64):
		attack_mask = bishop_masks[sq] if is_bishop else rook_masks[sq]

		relevant_bits_count = count_bits(attack_mask)
		occupancy_indices = 1 << relevant_bits_count

		for index in range(occupancy_indices):
			if is_bishop:  # bishop
				occupancy = set_occupancy(index, relevant_bits_count, attack_mask)
				magic_index = (occupancy * bishop_magic_numbers[sq]) >> np.ulonglong(64 - bishop_relevant_bits[sq])
				attacks[sq][magic_index] = bishop_attacks_with_occupancy(sq, occupancy)

			else:  # rook
				occupancy = set_occupancy(index, relevant_bits_count, attack_mask)
				magic_index = int((occupancy * rook_magic_numbers[sq]) >> np.ulonglong(64 - rook_relevant_bits[sq]))
				attacks[sq][magic_index] = rook_attacks_with_occupancy(sq, occupancy)

	return attacks

# sliders
bishop_attacks = init_sliders(np.empty((64, 512), dtype=np.ulonglong), is_bishop=True)
rook_attacks = init_sliders(np.empty((64, 4096), dtype=np.ulonglong), is_bishop=False)

# leapers
pawn_attacks = np.fromiter((mask_pawn_attacks(sq, color) for color in [white, black] for sq in range(64)), dtype=np.ulonglong)
pawn_attacks.shape = (2, 64)
knight_attacks = np.fromiter((mask_knight_attacks(sq) for sq in range(64)), dtype=np.ulonglong)
king_attacks = np.fromiter((mask_king_attacks(sq) for sq in range(64)), dtype=np.ulonglong)

def get_bishop_attacks(square: int, occupancy: np.ulonglong):
	if square == 63:
		return bishop_attacks_with_occupancy(square, occupancy)
	occupancy &= bishop_masks[square]
	occupancy *= bishop_magic_numbers[square]
	occupancy >>= np.ulonglong(64 - bishop_relevant_bits[square])
	return bishop_attacks[square][occupancy]

def get_rook_attacks(square: int, occupancy: np.ulonglong):
	occupancy &= rook_masks[square]
	occupancy *= rook_magic_numbers[square]
	occupancy >>= np.ulonglong(64 - rook_relevant_bits[square])
	return rook_attacks[square][occupancy]

def get_queen_attacks(square: int, occupancy: np.ulonglong):
	return get_rook_attacks(square, occupancy) | get_bishop_attacks(square, occupancy)

def get_attacks(piece, start_square, board, color):
    if piece == knight:
        return knight_attacks[start_square] & ~board.occupancy[color]
    elif piece == bishop:
        return get_bishop_attacks(start_square, board.occupancy[both]) & ~board.occupancy[color]
    elif piece == rook:
        return get_rook_attacks(start_square, board.occupancy[both]) & ~board.occupancy[color]
    elif piece == queen:
        return get_queen_attacks(start_square, board.occupancy[both]) & ~board.occupancy[color]
    elif piece == king:
        return king_attacks[start_square] & ~board.occupancy[color]

def is_square_attacked(board_state, square, color):
    """return True if the square is attacked by the given color else False"""
    opponent_color = color ^ 1
    if pawn_attacks[opponent_color][square] & board_state.pieces_bitboard[color][pawn] \
            or get_bishop_attacks(square, board_state.occupancy[both]) & board_state.pieces_bitboard[color][bishop] \
            or knight_attacks[square] & board_state.pieces_bitboard[color][knight] \
            or get_rook_attacks(square, board_state.occupancy[both]) & board_state.pieces_bitboard[color][rook] \
            or get_queen_attacks(square, board_state.occupancy[both]) & board_state.pieces_bitboard[color][queen] \
            or king_attacks[square] & board_state.pieces_bitboard[color][king]:
        return True
    return False