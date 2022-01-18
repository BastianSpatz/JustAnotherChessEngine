# this trigger the whole computatuon of look up tables
# from tables import *
from constants import *
from bitboard_utils import get_bit, set_bit
from move import Move

class Board():
	"""
		Represent the games chess board
			- Keep track of en-passant squares
			- Keep track of 
	"""
	def __init__(self):
		self.color = Color.WHITE

		self.en_passant_square = 64 # means no square

		self.is_checkmate = False
		self.is_stalemate = False

		""" 
		save this as a 4bit binary 
			0001    1  white king can castle to the king side
			0010    2  white king can castle to the queen side
			0100    4  black king can castle to the king side
			1000    8  black king can castle to the queen side
		"""
		self.castling_rights = {"wk": 1, "wq": 2, "bk": 4, "bq": 8} # TODO

		self._move_stack = []

		'''
			Define all the bitboards we need to keep track of:
		'''

		self.pieces_bitboard = np.zeros((2, 6), dtype=np.uint64)
		self.combined_pieces_bitboard = np.zeros(2, dtype=np.uint64)

		self.occupied_squares = EMPTY

		self.set_fen(STARTING_FEN)

	def __str__(self) -> None:
		output = "\n"
		for rank in range(BOARD_LENGTH):
			output += " "
			for file in range(BOARD_LENGTH):
				square = rank * 8 + file
				for color in Color:
					if get_bit(self.combined_pieces_bitboard[color], square):
						for piece in Piece:
							if get_bit(self.pieces_bitboard[color][piece], square):
								output += UNICODE_PIECE_SYMBOLS[piece.__to_symbol__(color)]
								break
						break
				else:
					output += '· '
			output += "\n" 
		output += " A B C D E F G H\n"
		return output
							

	def set_fen(self, fen) -> None:
		parts = fen.split()

		# Board part.
		try:
			board_part = parts.pop(0)
		except IndexError:
			raise ValueError("empty fen")

		if " " in board_part:
			raise ValueError(f"expected position part of fen, got multiple parts: {fen!r}")

		# Ensure the FEN is valid.
		rows = board_part.split("/")
		if len(rows) != 8:
			raise ValueError(f"expected 8 rows in position part of fen: {board_part!r}")

		# Validate each row.
		for row in rows:
			field_sum = 0
			previous_was_digit = False
			previous_was_piece = False

			for c in row:
				if c in ["1", "2", "3", "4", "5", "6", "7", "8"]:
					if previous_was_digit:
						raise ValueError(f"two subsequent digits in position part of fen: {board_part!r}")
					field_sum += int(c)
					previous_was_digit = True
					previous_was_piece = False
				elif c == "~":
					if not previous_was_piece:
						raise ValueError(f"'~' not after piece in position part of fen: {board_part!r}")
					previous_was_digit = False
					previous_was_piece = False
				elif c.lower() in PIECE_SYMBOLS:
					field_sum += 1
					previous_was_digit = False
					previous_was_piece = True
				else:
					raise ValueError(f"invalid character in position part of fen: {board_part!r}")

			if field_sum != 8:
				raise ValueError(f"expected 8 columns per row in position part of fen: {board_part!r}")

		self.clear_board()
		# Put pieces on the board.
		square_index = 0
		for c in board_part:
			if c == "w":
				self.color = Color.WHITE
			elif c == "b":
				self.color = Color.BLACK
			if c in ["1", "2", "3", "4", "5", "6", "7", "8"]:
				square_index += int(c)
			elif c.lower() in PIECE_SYMBOLS:
				piece, color = Piece.__from_symbol__(c)
				self.set_sq(SQUARES_180[square_index], piece, color)
				square_index += 1

	def set_sq(self, sq: int, piece: int, color=None) -> None:
		if color is None:
			color = self.color
		self.pieces_bitboard[color][piece] = set_bit(self.pieces_bitboard[color][piece], sq)
		self.combined_pieces_bitboard[color] = set_bit(self.combined_pieces_bitboard[color], sq)
		self.occupied_squares = set_bit(self.occupied_squares, sq)

	def clear_board(self):
		for color in Color:
			for piece in Piece:
				self.pieces_bitboard[color][piece] = EMPTY
			self.combined_pieces_bitboard[color] = EMPTY
		self.occupied_squares = EMPTY

	def generate_pseudo_legal_moves():
		"""return a list of pseudo legal moves"""
		move_list = []

		for piece in range(Piece):
			piece_bitboard = self.pieces_bitboard[self.color][piece]
			opponent_color = ~self.color

			# white pawns & castling
			if self.color == color.WHITE:
				if piece == piece.PAWN:
					while piece_bitboard:
						# white pawn move
						start_square = get_lsb1_index(piece_bitboard)
						target_square = start_square - 8

						#quiet pawn move
						if not (target_square < algebraic_square_map["a8"]) and not get_bit(self.occupied_squares, target_square):

							# promotion
							if algebraic_square_map["a7"] <= start_square <= algebraic_square_map["h7"]:
								move_list.append(Move(start_square, target_square, piece, self.color, Piece.QUEEN, 0, 0, 0, 0))
								move_list.append(Move(start_square, target_square, piece, self.color, Piece.ROOK, 0, 0, 0, 0))
								move_list.append(Move(start_square, target_square, piece, self.color, Piece.BISHOP, 0, 0, 0, 0))
								move_list.append(Move(start_square, target_square, piece, self.color, Piece.KNIGHT, 0, 0, 0, 0))

							else:
								# pawn push
								move_list.append(Move(start_square, target_square, piece, self.color, 0, 0, 0, 0, 0))

								# pawn double push
								if algebraic_square_map["a2"] <= start_square <= algebraic_square_map["h2"] and not get_bit(self.occupied_squares, target_square - 8):
									move_list.append(Move(start_square, target_square - 8, piece, self.color, 0, 0, 1, 0, 0))






		
class BoardState():
	"""
		Represent a Chess position
	"""
	def __init__(self):
		pass
		