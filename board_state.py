import numpy as np
from dataclasses import dataclass, field
import re

from bitboard_utils import get_bit, set_bit
from constants import *

@dataclass()
class BoardState:
    """Store a BoardState"""
    color: int = field(init=False)

    en_passant_square: int = field(init=False)

    castle: int  = field(init=False)

    pieces_bitboard: np.ndarray = field(init=False)
    occupancy: np.ndarray = field(init=False)

    def __post_init__(self):
        self.color = 0

        self.en_passant_square = 64

        self.castle = 0

        self.pieces_bitboard = np.zeros((2, 6), dtype=np.ulonglong)
        self.occupancy = np.zeros(3, dtype=np.ulonglong)




###########################################
#           board_state utils             #
###########################################

def print_board_state(board_state):
    output = "\n"
    for rank in range(8):
        output += str(8-rank) + " "
        for file in range(8):
            square = rank * 8 + file
            for color in [white, black]:
                if get_bit(board_state.occupancy[color], square):
                    for piece in Pieces:
                        if get_bit(board_state.pieces_bitboard[color][piece], square):
                            output += " " + UNICODE_PIECE_SYMBOLS[PIECE_SYMBOLS[piece + 6*color]]
                            break
                    break
            else:
                output += ' · '
        output += "\n" 
    output += "   A  B  C  D  E  F  G  H\n"
    output += "Side:     \n" + str(board_state.color) + "\n"
    output += "Enpassant:   \n" 
    output += "- \n" if board_state.en_passant_square == 64 else str(board_state.en_passant_square) + ": " + square_to_coordinates[board_state.en_passant_square] + "\n"
    output += "Castling:    \n" 
    castle = (
        f"{'K' if board_state.castle & wk else ''}{'Q' if board_state.castle & wq else ''}"
        f"{'k' if board_state.castle & bk else ''}{'q' if board_state.castle & bq else ''} "
    )
    output += castle if castle else "-"

    print(output)

def set_fen(fen) -> None:
    board_state = BoardState()
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
        board_state.color = Color.WHITE
    else:
        if turn_part == "w":
            board_state.color = 0
        elif turn_part == "b":
            board_state.color = 1
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
        board_state.en_passant_square = None
    else:
        try:
            board_state.en_passant_square = 64 if ep_part == "-" else square_to_coordinates.index(ep_part)
        except ValueError:
            raise ValueError(f"invalid en passant part in fen: {fen!r}")    

    castling_part = list(castling_part)
    board_state.castle = 0
    for i in range(len(castling_part)):
        if castling_part[i] == "K":
            board_state.castle |= wk
        elif castling_part[i] == "Q":
            board_state.castle |= wq
        elif castling_part[i] == "k":
            board_state.castle |= bk
        elif castling_part[i] == "q":
            board_state.castle |= bq

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
    for color in [white, black]:
        for piece in Pieces:
            board_state.pieces_bitboard[color][piece] = EMPTY
        board_state.occupancy[color] = EMPTY
    board_state.occupancy[both] = EMPTY

    # Put pieces on the board.
    square_index = 0
    for c in board_part:
        if c in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            square_index += int(c)
        elif c in PIECE_SYMBOLS:
            piece, color = piece_from_symbol(c)

            board_state.pieces_bitboard[color][piece] = set_bit(board_state.pieces_bitboard[color][piece], square_index)
            board_state.occupancy[color] = set_bit(board_state.occupancy[color], square_index)
            board_state.occupancy[both] = set_bit(board_state.occupancy[both], square_index)

            square_index += 1

    return board_state


