import numpy as np

from board import Board
from board_state import BoardState
from move import Move
from bitboard_utils import print_bb, set_bit, pop_bit, get_lsb1_index
from constants import Piece, Color, algebraic_square_map, square_to_coordinates, castling_rights, wk, wq, bk, bq
from tables import bishop_attacks, rook_attacks, pawn_attacks, knight_attacks, king_attacks, is_square_attacked, get_attacks
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
                            move_list.append(Move(start_square, target_square, piece, Color.WHITE, Piece.QUEEN, 0, 0, 0, 0))
                            move_list.append(Move(start_square, target_square, piece, Color.WHITE, Piece.ROOK, 0, 0, 0, 0))
                            move_list.append(Move(start_square, target_square, piece, Color.WHITE, Piece.BISHOP, 0, 0, 0, 0))
                            move_list.append(Move(start_square, target_square, piece, Color.WHITE, Piece.KNIGHT, 0, 0, 0, 0))
                            # print("queen promotion: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            # print("rook promotion: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            # print("bishop promotion: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            # print("knight promotion: ", square_to_coordinates[start_square], square_to_coordinates[target_square])

                        else:
                            # pawn push
                            # print("pawn push: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            move_list.append(Move(start_square, target_square, piece, Color.WHITE, 0, 0, 0, 0, 0))
                        if algebraic_square_map["a2"] <= start_square <= algebraic_square_map["h2"] and not get_bit(board.occupied_squares, target_square - 8):
                            move_list.append(Move(start_square, target_square-8, piece, Color.WHITE, 0, 0, 1, 0, 0))
                            # print("double pawn push: ", square_to_coordinates[start_square], square_to_coordinates[target_square-8])

                    attacks = pawn_attacks[Color.WHITE][start_square] & board.combined_pieces_bitboard[Color.BLACK]

                    while attacks:
                        target_square = get_lsb1_index(attacks)
                        # promotion capture
                        if algebraic_square_map["a7"] <= start_square <= algebraic_square_map["h7"]:
                            move_list.append(Move(start_square, target_square, piece, Color.WHITE, Piece.QUEEN, 1, 0, 0, 0))
                            move_list.append(Move(start_square, target_square, piece, Color.WHITE, Piece.ROOK, 1, 0, 0, 0))
                            move_list.append(Move(start_square, target_square, piece, Color.WHITE, Piece.BISHOP, 1, 0, 0, 0))
                            move_list.append(Move(start_square, target_square, piece, Color.WHITE, Piece.KNIGHT, 1, 0, 0, 0))
                            # print("queen promotion capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            # print("rook promotion capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            # print("bishop promotion capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            # print("knight promotion capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])

                        else:
                            # pawn push
                            # print("pawn capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            move_list.append(Move(start_square, target_square, piece, Color.WHITE, 0, 1, 0, 0, 0))
                        attacks = pop_bit(attacks, target_square)

                    if board.en_passant_square != 64:
                        en_passant_attacks = pawn_attacks[Color.WHITE][start_square] & np.ulonglong(1 << board.en_passant_square)
                        if en_passant_attacks:
                            target_en_passant = get_lsb1_index(en_passant_attacks)
                            move_list.append(Move(start_square, target_en_passant, piece, Color.WHITE, 0, 1, 0, 1, 0))
                            # print("en passant capture: ", square_to_coordinates[start_square], square_to_coordinates[target_en_passant])
                    piece_bitboard = pop_bit(piece_bitboard, start_square)
            # castle moves
            elif piece == Piece.KING:
                # kingside castle
                if board.castle & wk:
                    if not get_bit(board.occupied_squares, algebraic_square_map["f1"]) and not get_bit(board.occupied_squares, algebraic_square_map["g1"]):
                        if not is_square_attacked(algebraic_square_map["e1"], board, Color.BLACK) and not is_square_attacked(algebraic_square_map["f1"], board, Color.BLACK):
                            # print("castling move: e1g1")
                            move_list.append(Move(algebraic_square_map["e1"], algebraic_square_map["g1"], piece, Color.WHITE, 0, 0, 0, 0, 1))
                if board.castle & wq:
                    if not get_bit(board.occupied_squares, algebraic_square_map["d1"]) and not get_bit(board.occupied_squares, algebraic_square_map["c1"]) and not get_bit(board.occupied_squares, algebraic_square_map["b1"]):
                        if not is_square_attacked(algebraic_square_map["d1"], board, Color.BLACK) and not is_square_attacked(algebraic_square_map["e1"], board, Color.BLACK):
                            move_list.append(Move(algebraic_square_map["e1"], algebraic_square_map["c1"], piece, Color.WHITE, 0, 0, 0, 0, 1))
                            # print("castling move: e1c1")

            # knight moves
            elif piece == Piece.KNIGHT:
                while piece_bitboard:
                    start_square = get_lsb1_index(piece_bitboard)

                    attacks = get_attacks(piece, start_square, board, Color.WHITE)
                    while attacks:
                        target_square = get_lsb1_index(attacks)
                        if not get_bit(board.combined_pieces_bitboard[Color.BLACK], target_square):
                            move_list.append(Move(start_square, target_square, piece, Color.WHITE, 0, 0, 0, 0, 0))
                            # print("knight move: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                        else:
                            move_list.append(Move(start_square, target_square, piece, Color.WHITE, 0, 1, 0, 0, 0))
                            # print("knight capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])

                        attacks = pop_bit(attacks, target_square)
                    piece_bitboard = pop_bit(piece_bitboard, start_square)

            # rook moves
            elif piece == Piece.ROOK:
                while piece_bitboard:
                    start_square = get_lsb1_index(piece_bitboard)

                    attacks = get_attacks(piece, start_square, board, Color.WHITE)
                    while attacks:
                        target_square = get_lsb1_index(attacks)
                        if not get_bit(board.combined_pieces_bitboard[Color.BLACK], target_square):
                            move_list.append(Move(start_square, target_square, piece, Color.WHITE, 0, 0, 0, 0, 0))
                            # print("rook move: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                        else:
                            move_list.append(Move(start_square, target_square, piece, Color.WHITE, 0, 1, 0, 0, 0))
                            # print("rook capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])

                        attacks = pop_bit(attacks, target_square)
                    piece_bitboard = pop_bit(piece_bitboard, start_square)

            # bishop moves
            elif piece == Piece.BISHOP:
                while piece_bitboard:
                    start_square = get_lsb1_index(piece_bitboard)

                    attacks = get_attacks(piece, start_square, board, Color.WHITE)
                    while attacks:
                        target_square = get_lsb1_index(attacks)
                        if not get_bit(board.combined_pieces_bitboard[Color.BLACK], target_square):
                            move_list.append(Move(start_square, target_square, piece, Color.WHITE, 0, 0, 0, 0, 0))
                            # print("bishop move: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                        else:
                            move_list.append(Move(start_square, target_square, piece, Color.WHITE, 0, 1, 0, 0, 0))
                            # print("bishop capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])

                        attacks = pop_bit(attacks, target_square)
                    piece_bitboard = pop_bit(piece_bitboard, start_square)

            # queen moves
            elif piece == Piece.QUEEN:
                while piece_bitboard:
                    start_square = get_lsb1_index(piece_bitboard)

                    attacks = get_attacks(piece, start_square, board, Color.WHITE)
                    while attacks:
                        target_square = get_lsb1_index(attacks)
                        if not get_bit(board.combined_pieces_bitboard[Color.BLACK], target_square):
                            move_list.append(Move(start_square, target_square, piece, Color.WHITE, 0, 0, 0, 0, 0))
                            # print("queen move: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                        else:
                            move_list.append(Move(start_square, target_square, piece, Color.WHITE, 0, 1, 0, 0, 0))
                            # print("queen capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])

                        attacks = pop_bit(attacks, target_square)
                    piece_bitboard = pop_bit(piece_bitboard, start_square)

            # king moves
            if piece == Piece.KING:
                while piece_bitboard:
                    start_square = get_lsb1_index(piece_bitboard)

                    attacks = get_attacks(piece, start_square, board, Color.WHITE)
                    while attacks:
                        target_square = get_lsb1_index(attacks)
                        if not get_bit(board.combined_pieces_bitboard[Color.BLACK], target_square):
                            move_list.append(Move(start_square, target_square, piece, Color.WHITE, 0, 0, 0, 0, 0))
                            # print("king move: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                        else:
                            move_list.append(Move(start_square, target_square, piece, Color.WHITE, 0, 1, 0, 0, 0))
                            # print("king capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])

                        attacks = pop_bit(attacks, target_square)
                    piece_bitboard = pop_bit(piece_bitboard, start_square)

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
                            move_list.append(Move(start_square, target_square, piece, Color.BLACK, Piece.QUEEN, 0, 0, 0, 0))
                            move_list.append(Move(start_square, target_square, piece, Color.BLACK, Piece.ROOK, 0, 0, 0, 0))
                            move_list.append(Move(start_square, target_square, piece, Color.BLACK, Piece.BISHOP, 0, 0, 0, 0))
                            move_list.append(Move(start_square, target_square, piece, Color.BLACK, Piece.KNIGHT, 0, 0, 0, 0))
                            # print("queen promotion: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            # print("rook promotion: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            # print("bishop promotion: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            # print("knight promotion: ", square_to_coordinates[start_square], square_to_coordinates[target_square])

                        else:
                            # pawn push
                            move_list.append(Move(start_square, target_square, piece, Color.BLACK, 0, 0, 0, 0, 0))
                            # print("pawn push: ", square_to_coordinates[start_square], square_to_coordinates[target_square])

                        if algebraic_square_map["a7"] <= start_square <= algebraic_square_map["h7"] and not get_bit(board.occupied_squares, target_square + 8):
                            move_list.append(Move(start_square, target_square + 8, piece, Color.BLACK, 0, 0, 1, 0, 0))
                            # print("double pawn push: ", square_to_coordinates[start_square], square_to_coordinates[target_square+8])

                    attacks = pawn_attacks[Color.BLACK][start_square] & board.combined_pieces_bitboard[Color.WHITE]

                    while attacks:
                        target_square = get_lsb1_index(attacks)
                        # promotion
                        if algebraic_square_map["a2"] <= start_square <= algebraic_square_map["h2"]:
                            # print("queen promotion capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            # print("rook promotion capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            # print("bishop promotion capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            # print("knight promotion capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            move_list.append(Move(start_square, target_square, piece, Color.BLACK, Piece.QUEEN, 1, 0, 0, 0))
                            move_list.append(Move(start_square, target_square, piece, Color.BLACK, Piece.ROOK, 1, 0, 0, 0))
                            move_list.append(Move(start_square, target_square, piece, Color.BLACK, Piece.BISHOP, 1, 0, 0, 0))
                            move_list.append(Move(start_square, target_square, piece, Color.BLACK, Piece.KNIGHT, 1, 0, 0, 0))

                        else:
                            # pawn push
                            # print("pawn capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            move_list.append(Move(start_square, target_square, piece, Color.BLACK, 0, 1, 0, 0, 0))

                        attacks = pop_bit(attacks, target_square)

                    if board.en_passant_square != 64:
                        en_passant_attacks = pawn_attacks[Color.BLACK][start_square] & np.ulonglong(1 << board.en_passant_square)
                        if en_passant_attacks:
                            target_en_passant = get_lsb1_index(en_passant_attacks)
                            # print("en passant capture: ", square_to_coordinates[start_square], square_to_coordinates[target_en_passant])
                            move_list.append(Move(start_square, target_en_passant, piece, Color.BLACK, 0, 1, 0, 1, 0))
                    
                    piece_bitboard = pop_bit(piece_bitboard, start_square)

            # castle moves
            elif piece == Piece.KING:
                # kingside castle
                if board.castle & bk:
                    if not get_bit(board.occupied_squares, algebraic_square_map["f8"]) and not get_bit(board.occupied_squares, algebraic_square_map["g8"]):
                        if not is_square_attacked(algebraic_square_map["e8"], board, Color.WHITE) and not is_square_attacked(algebraic_square_map["f8"], board, Color.WHITE):
                            # print("castling move: e8g8")
                            move_list.append(Move(algebraic_square_map["e8"], algebraic_square_map["g8"], piece, Color.BLACK, 0, 0, 0, 0, 1))
                if board.castle & bq:
                    if not get_bit(board.occupied_squares, algebraic_square_map["d8"]) and not get_bit(board.occupied_squares, algebraic_square_map["c8"]) and not get_bit(board.occupied_squares, algebraic_square_map["b8"]):
                        if not is_square_attacked(algebraic_square_map["d8"], board, Color.WHITE) and not is_square_attacked(algebraic_square_map["e8"], board, Color.WHITE):
                            # print("castling move: e8c8")
                            move_list.append(Move(algebraic_square_map["e8"], algebraic_square_map["c8"], piece, Color.BLACK, 0, 0, 0, 0, 1))

            # knight moves
            elif piece == Piece.KNIGHT:
                while piece_bitboard:
                    start_square = get_lsb1_index(piece_bitboard)

                    attacks = get_attacks(piece, start_square, board, Color.BLACK)
                    while attacks:
                        target_square = get_lsb1_index(attacks)
                        if not get_bit(board.combined_pieces_bitboard[Color.WHITE], target_square):
                            # print("knight move: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            move_list.append(Move(start_square, target_square, piece, Color.BLACK, 0, 0, 0, 0, 0))
                        else:
                            # print("knight capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            move_list.append(Move(start_square, target_square, piece, Color.BLACK, 0, 1, 0, 0, 0))

                        attacks = pop_bit(attacks, target_square)
                    piece_bitboard = pop_bit(piece_bitboard, start_square)

            # rook moves
            elif piece == Piece.ROOK:
                while piece_bitboard:
                    start_square = get_lsb1_index(piece_bitboard)

                    attacks = get_attacks(piece, start_square, board, Color.BLACK)
                    while attacks:
                        target_square = get_lsb1_index(attacks)
                        if not get_bit(board.combined_pieces_bitboard[Color.WHITE], target_square):
                            # print("rook move: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            move_list.append(Move(start_square, target_square, piece, Color.BLACK, 0, 0, 0, 0, 0))
                        else:
                            # print("rook capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            move_list.append(Move(start_square, target_square, piece, Color.BLACK, 0, 1, 0, 0, 0))

                        attacks = pop_bit(attacks, target_square)
                    piece_bitboard = pop_bit(piece_bitboard, start_square)

            # bishop moves
            elif piece == Piece.BISHOP:
                while piece_bitboard:
                    start_square = get_lsb1_index(piece_bitboard)

                    attacks = get_attacks(piece, start_square, board, Color.BLACK)
                    while attacks:
                        target_square = get_lsb1_index(attacks)
                        if not get_bit(board.combined_pieces_bitboard[Color.WHITE], target_square):
                            # print("bishop move: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            move_list.append(Move(start_square, target_square, piece, Color.BLACK, 0, 0, 0, 0, 0))
                        else:
                            # print("bishop capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            move_list.append(Move(start_square, target_square, piece, Color.BLACK, 0, 1, 0, 0, 0))

                        attacks = pop_bit(attacks, target_square)
                    piece_bitboard = pop_bit(piece_bitboard, start_square)

            # queen moves
            elif piece == Piece.QUEEN:
                while piece_bitboard:
                    start_square = get_lsb1_index(piece_bitboard)

                    attacks = get_attacks(piece, start_square, board, Color.BLACK)
                    while attacks:
                        target_square = get_lsb1_index(attacks)
                        if not get_bit(board.combined_pieces_bitboard[Color.WHITE], target_square):
                            # print("queen move: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            move_list.append(Move(start_square, target_square, piece, Color.BLACK, 0, 0, 0, 0, 0))
                        else:
                            # print("queen capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            move_list.append(Move(start_square, target_square, piece, Color.BLACK, 0, 1, 0, 0, 0))

                        attacks = pop_bit(attacks, target_square)
                    piece_bitboard = pop_bit(piece_bitboard, start_square)

            # king moves
            if piece == Piece.KING:
                while piece_bitboard:
                    start_square = get_lsb1_index(piece_bitboard)

                    attacks = get_attacks(piece, start_square, board, Color.BLACK)
                    while attacks:
                        target_square = get_lsb1_index(attacks)
                        if not get_bit(board.combined_pieces_bitboard[Color.WHITE], target_square):
                            # print("king move: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            move_list.append(Move(start_square, target_square, piece, Color.BLACK, 0, 0, 0, 0, 0))
                        else:
                            # print("king capture: ", square_to_coordinates[start_square], square_to_coordinates[target_square])
                            move_list.append(Move(start_square, target_square, piece, Color.BLACK, 0, 1, 0, 0, 0))

                        attacks = pop_bit(attacks, target_square)
                    piece_bitboard = pop_bit(piece_bitboard, start_square)

    return move_list

def make_move(board_state_orig, move, only_captures = False):
    board_state = BoardState()
    board_state.read_board(board_state_orig)

    if not only_captures:

        start_square = move.get_move_source()
        target_square = move.get_move_target()
        piece = move.get_move_piece()
        color = int(move.get_move_color())
        opp_color = color ^ 1

        promoted_piece = move.get_move_promote_to()  
        capture_flag = move.get_move_capture()
        double_push_flag = move.get_move_double()
        enpassant_flag = move.get_move_enpassant()
        castling_flag = move.get_move_castling()

        # set bits in the piece bitboard
        board_state.pieces_bitboard[color][piece] = pop_bit(board_state.pieces_bitboard[color][piece], start_square)
        board_state.pieces_bitboard[color][piece] = set_bit(board_state.pieces_bitboard[color][piece], target_square)

        # #set piece in the combines bitboard
        # board_state.combined_pieces_bitboard[color] = pop_bit(board_state.combined_pieces_bitboard[color], start_square)
        # board_state.combined_pieces_bitboard[color] = set_bit(board_state.combined_pieces_bitboard[color], target_square)

        # #set piece in the occ
        # board_state.occupied_squares = pop_bit(board_state.occupied_squares, start_square)
        # board_state.occupied_squares = set_bit(board_state.occupied_squares, target_square)

        if capture_flag:
            for piece in Piece:
                if get_bit(board_state.pieces_bitboard[opp_color][piece], target_square):
                    # pop bits in the piece bitboard
                    board_state.pieces_bitboard[opp_color][piece] = pop_bit(board_state.pieces_bitboard[opp_color][piece], target_square)
                    break

        if promoted_piece:
            # pop bits in the piece bitboard
            board_state.pieces_bitboard[opp_color][piece] = pop_bit(board_state.pieces_bitboard[opp_color][piece], target_square)


            # set bits in the piece bitboard
            board_state.pieces_bitboard[color][promoted_piece] = set_bit(board_state.pieces_bitboard[color][promoted_piece], target_square)

        if enpassant_flag: #capture en passant 
            if color: # black moved the pawn
               # pop bits in the piece bitboard
                board_state.pieces_bitboard[opp_color][piece] = pop_bit(board_state.pieces_bitboard[opp_color][piece], target_square - 8) 
            else:
               # pop bits in the piece bitboard
                board_state.pieces_bitboard[opp_color][piece] = pop_bit(board_state.pieces_bitboard[opp_color][piece], target_square + 8)

        board_state.en_passant_square = 64

        if double_push_flag:
            if color: 
                board_state.en_passant_square = target_square - 8 
            else:
               # pop bits in the piece bitboard
                board_state.en_passant_square = target_square + 8 

        if castling_flag:
            if target_square == algebraic_square_map["g1"]:
                board_state.pieces_bitboard[color][Piece.ROOK] = pop_bit(board_state.pieces_bitboard[color][Piece.ROOK], algebraic_square_map["h1"])

                board_state.pieces_bitboard[color][Piece.ROOK] = set_bit(board_state.pieces_bitboard[color][Piece.ROOK], algebraic_square_map["f1"])

            elif target_square == algebraic_square_map["c1"]:
                board_state.pieces_bitboard[color][Piece.ROOK] = pop_bit(board_state.pieces_bitboard[color][Piece.ROOK], algebraic_square_map["a1"])

                board_state.pieces_bitboard[color][Piece.ROOK] = set_bit(board_state.pieces_bitboard[color][Piece.ROOK], algebraic_square_map["d1"])

            elif target_square == algebraic_square_map["g8"]:
                board_state.pieces_bitboard[color][Piece.ROOK] = pop_bit(board_state.pieces_bitboard[color][Piece.ROOK], algebraic_square_map["h8"])

                board_state.pieces_bitboard[color][Piece.ROOK] = set_bit(board_state.pieces_bitboard[color][Piece.ROOK], algebraic_square_map["f8"])

            elif target_square == algebraic_square_map["c8"]:
                board_state.pieces_bitboard[color][Piece.ROOK] = pop_bit(board_state.pieces_bitboard[color][Piece.ROOK], algebraic_square_map["a8"])

                board_state.pieces_bitboard[color][Piece.ROOK] = set_bit(board_state.pieces_bitboard[color][Piece.ROOK], algebraic_square_map["d8"])


        # update castling rights
        board_state.castle &= castling_rights[start_square]
        board_state.castle &= castling_rights[target_square]

        # update occ
        for c in Color:
            for bb in board_state.pieces_bitboard[c]:
                board_state.combined_pieces_bitboard[c] |= bb
            board_state.occupied_squares |= board_state.combined_pieces_bitboard[c]

        board_state.color = opp_color

        if not is_square_attacked(get_lsb1_index(board_state.pieces_bitboard[color][Piece.KING]), board_state, opp_color):
            return board_state

    else:
        if move.get_move_capture():
            return make_move(board_state, move, False)
        return None

    return None







