import numpy as np

from bitboard_utils import print_bb
from constants import Piece, Color, algebraic_square_map, square_to_coordinates
from tables import bishop_attacks, rook_attacks, pawn_attacks, knight_attacks, king_attacks, is_square_attacked
from bitboard_utils import get_lsb1_index, get_bit, pop_bit, print_bb, count_bits

"""
           Binary move bits             Meaning          Hexadecimal
    0000 0000 0000 0000 0011 1111    start square        0x3f
    0000 0000 0000 1111 1100 0000    target square       0xfc0
    0000 0000 0111 0000 0000 0000    piece               0x7000
    0000 0000 1000 0000 0000 0000    side                0x8000
    0000 1111 0000 0000 0000 0000    promoted piece      0xf0000
    0001 0000 0000 0000 0000 0000    capture flag        0x100000
    0010 0000 0000 0000 0000 0000    double push flag    0x200000
    0100 0000 0000 0000 0000 0000    enpassant flag      0x400000
    1000 0000 0000 0000 0000 0000    castling flag       0x800000
"""

def generate_pseudo_legal_moves(board):
    """return a list of pseudo legal moves"""
    move_list = []

    for piece in Piece:
        piece_bitboard = board.pieces_bitboard[board.color][piece]

        if board.color == Color.WHITE:
            if piece == Piece.PAWN:
                while piece_bitboard:
                    # white pawn move
                    start_square = get_lsb1_index(piece_bitboard)
                    target_square = start_square - 8

                    #quiet pawn move
                    if not (target_square < algebraic_square_map["a8"]) and not get_bit(board.occupied_squares, target_square):

                      # promotion
                        if algebraic_square_map["a7"] <= start_square <= algebraic_square_map["h7"]:
                            print("queen promotion: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            print("rook promotion: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            print("bishop promotion: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            print("knight promotion: ", square_to_coordinates[start_square], square_to_coordinates[target_square])

                        else:
                            # pawn push
                            print("pawn push: ", square_to_coordinates[start_square], square_to_coordinates[target_square])

                        if algebraic_square_map["a2"] <= start_square <= algebraic_square_map["h2"] and not get_bit(board.occupied_squares, target_square - 8):
                            print("double pawn push: ", square_to_coordinates[start_square], square_to_coordinates[target_square-8])

                    attacks = pawn_attacks[Color.WHITE][start_square] & board.combined_pieces_bitboard[Color.BLACK]

                    while attacks:
                        target_square = get_lsb1_index(attacks)
                        # promotion
                        if algebraic_square_map["a7"] <= start_square <= algebraic_square_map["h7"]:
                            print("queen promotion capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            print("rook promotion capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            print("bishop promotion capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            print("knight promotion capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])

                        else:
                            # pawn push
                            print("pawn capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])

                        attacks = pop_bit(attacks, target_square)

                    if board.en_passant_square != 64:
                        en_passant_attacks = pawn_attacks[Color.WHITE][start_square] & np.ulonglong(1 << board.en_passant_square)
                        if en_passant_attacks:
                            target_en_passant = get_lsb1_index(en_passant_attacks)
                            print("en passant capture: ", square_to_coordinates[start_square], square_to_coordinates[target_en_passant])
                    piece_bitboard = pop_bit(piece_bitboard, start_square)
            # castle moves
            elif piece == Piece.KING:
                # kingside castle
                if board.castle["wk"]==1:
                    if not get_bit(board.occupied_squares, algebraic_square_map["f1"]) and not get_bit(board.occupied_squares, algebraic_square_map["g1"]):
                        if not is_square_attacked(algebraic_square_map["e1"], board, Color.BLACK) and not is_square_attacked(algebraic_square_map["f1"], board, Color.BLACK):
                            print("castling move: e1g1")
                if board.castle["wq"]==1:
                    if not get_bit(board.occupied_squares, algebraic_square_map["d1"]) and not get_bit(board.occupied_squares, algebraic_square_map["c1"]) and not get_bit(board.occupied_squares, algebraic_square_map["b1"]):
                        if not is_square_attacked(algebraic_square_map["d1"], board, Color.BLACK) and not is_square_attacked(algebraic_square_map["e1"], board, Color.BLACK):
                            print("castling move: e1c1")



        # black pieces
        else:
            if piece == Piece.PAWN:
                while piece_bitboard:
                    # black pawn move
                    start_square = get_lsb1_index(piece_bitboard)
                    target_square = start_square + 8

                    #quiet pawn move
                    if not (target_square > algebraic_square_map["h1"]) and not get_bit(board.occupied_squares, target_square):

                      # promotion
                        if algebraic_square_map["a2"] <= start_square <= algebraic_square_map["h2"]:
                            print("queen promotion: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            print("rook promotion: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            print("bishop promotion: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            print("knight promotion: ", square_to_coordinates[start_square], square_to_coordinates[target_square])

                        else:
                            # pawn push
                            print("pawn push: ", square_to_coordinates[start_square], square_to_coordinates[target_square])

                        if algebraic_square_map["a7"] <= start_square <= algebraic_square_map["h7"] and not get_bit(board.occupied_squares, target_square + 8):
                            print("double pawn push: ", square_to_coordinates[start_square], square_to_coordinates[target_square+8])

                    attacks = pawn_attacks[Color.BLACK][start_square] & board.combined_pieces_bitboard[Color.WHITE]

                    while attacks:
                        target_square = get_lsb1_index(attacks)
                        # promotion
                        if algebraic_square_map["a2"] <= start_square <= algebraic_square_map["h2"]:
                            print("queen promotion capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            print("rook promotion capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            print("bishop promotion capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            print("knight promotion capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])

                        else:
                            # pawn push
                            print("pawn capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])

                        attacks = pop_bit(attacks, target_square)

                    if board.en_passant_square != 64:
                        en_passant_attacks = pawn_attacks[Color.BLACK][start_square] & np.ulonglong(1 << board.en_passant_square)
                        if en_passant_attacks:
                            target_en_passant = get_lsb1_index(en_passant_attacks)
                            print("en passant capture: ", square_to_coordinates[start_square], square_to_coordinates[target_en_passant])
                    
                    piece_bitboard = pop_bit(piece_bitboard, start_square)

    return move_list