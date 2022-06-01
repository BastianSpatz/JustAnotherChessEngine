# this trigger the whole computatuon of look up tables
# from tables import *
import re
from constants import *
from bitboard_utils import get_bit, set_bit

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
        # self.castle = np.uint8(0)
        self.castle = 0#{"wk": 0, "wq": 0, "bk": 0, "bq": 0}

        self._board_states = []

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
            output += str(8-rank) + " "
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
        output += "  A B C D E F G H\n"
        output += "Side:     \n" + str(self.color) + "\n"
        output += "Enpassant:   \n" 
        output += "no \n" if self.en_passant_square == 64 else str(self.en_passant_square) + ": " + square_to_coordinates[self.en_passant_square] + "\n"
        output += "Castling:    \n" 
        castle = (
            f"{'K' if self.castle & wk else ''}{'Q' if self.castle & wq else ''}"
            f"{'k' if self.castle & bk else ''}{'q' if self.castle & bq else ''} "
        )
        output += castle if castle else "-"
        # output += "K" if (self.castle["wk"] == 1) else '-' 
        # output += "Q" if (self.castle["wq"] == 1) else '-' 
        # output += "k" if (self.castle["bk"] == 1) else '-' 
        # output += "q" if (self.castle["bq"] == 1) else '-'

        return output

    def set_board_state(self, board_state):
        self.pieces_bitboard = board_state.pieces_bitboard
        self.combined_pieces_bitboard = board_state.combined_pieces_bitboard
        self.occupied_squares = board_state.occupied_squares

        self.color = board_state.color
        self.en_passant_square = board_state.en_passant_square
        self.castle = board_state.castle                  

    def set_fen(self, fen) -> None:
        parts = fen.split()

        # Board part.
        try:
            board_part = parts.pop(0)
        except IndexError:
            raise ValueError("empty fen")

        # Turn.
        try:
            turn_part = parts.pop(0)
        except IndexError:
            self.color = Color.WHITE
        else:
            if turn_part == "w":
                self.color = Color.WHITE
            elif turn_part == "b":
                self.color = Color.BLACK
            else:
                raise ValueError(f"expected 'w' or 'b' for turn part of fen: {fen!r}")

        # Validate castling part.
        try:
            castling_part = parts.pop(0)
        except IndexError:
            castling_part = "-"
        else:
            if not re.compile(r"^(?:-|[KQABCDEFGH]{0,2}[kqabcdefgh]{0,2})\Z").match(castling_part):
                raise ValueError(f"invalid castling part in fen: {fen!r}")  

        # En passant square.
        try:
            ep_part = parts.pop(0)
        except IndexError:
            self.en_passant_square = None
        else:
            try:
                self.en_passant_square = 64 if ep_part == "-" else square_to_coordinates.index(ep_part)
            except ValueError:
                raise ValueError(f"invalid en passant part in fen: {fen!r}")    

        castling_part = list(castling_part)
        self.castle = 0
        for i in range(len(castling_part)):
            if castling_part[i] == "K":
                self.castle |= wk
            elif castling_part[i] == "Q":
                self.castle |= wq
            elif castling_part[i] == "k":
                self.castle |= bk
            elif castling_part[i] == "q":
                self.castle |= bq

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

        # clear board
        for color in Color:
            for piece in Piece:
                self.pieces_bitboard[color][piece] = EMPTY
            self.combined_pieces_bitboard[color] = EMPTY
        self.occupied_squares = EMPTY

        # Put pieces on the board.
        square_index = 0
        for c in board_part:
            # if c == "w":
            #   self.color = Color.WHITE
            # elif c == "b":
            #   self.color = Color.BLACK
            if c in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                square_index += int(c)
            elif c in PIECE_SYMBOLS:
                piece, color = Piece.__from_symbol__(c)

                self.pieces_bitboard[color][piece] = set_bit(self.pieces_bitboard[color][piece], square_index)
                self.combined_pieces_bitboard[color] = set_bit(self.combined_pieces_bitboard[color], square_index)
                self.occupied_squares = set_bit(self.occupied_squares, square_index)

                square_index += 1



        