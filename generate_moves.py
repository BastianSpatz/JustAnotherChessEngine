import numpy as np

# from board import Board
from board_state import BoardState
from move import *
from bitboard_utils import get_bit, set_bit, pop_bit, get_lsb1_index, print_bitboard
from constants import *
from tables import bishop_attacks, rook_attacks, pawn_attacks, knight_attacks, king_attacks, is_square_attacked, get_attacks

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

def generate_pseudo_legal_moves(board_state):
    """return a list of pseudo legal moves"""
    move_list = []

    for piece in Pieces:
        piece_bitboard = board_state.pieces_bitboard[board_state.color][piece]
        opp_color = board_state.color ^ 1

        if board_state.color == white:
            if piece == pawn:
                while piece_bitboard:
                    # white pawn move
                    start_square = get_lsb1_index(piece_bitboard)
                    target_square = start_square - 8

                    #quiet pawn move
                    if not (target_square < a8) and not get_bit(board_state.occupancy[both], target_square):

                      # promotion
                        if a7 <= start_square <= h7:
                            move_list.append(encode_move(start_square, target_square, piece, board_state.color, queen, 0, 0, 0, 0))
                            move_list.append(encode_move(start_square, target_square, piece, board_state.color, rook, 0, 0, 0, 0))
                            move_list.append(encode_move(start_square, target_square, piece, board_state.color, bishop, 0, 0, 0, 0))
                            move_list.append(encode_move(start_square, target_square, piece, board_state.color, knight, 0, 0, 0, 0))

                        else:
                            move_list.append(encode_move(start_square, target_square, piece, board_state.color, 0, 0, 0, 0, 0))

                            if a2 <= start_square <= h2 and not get_bit(board_state.occupancy[both], target_square - 8):
                                move_list.append(encode_move(start_square, target_square-8, piece, board_state.color, 0, 0, 1, 0, 0))
                                
                    attacks = pawn_attacks[white][start_square] & board_state.occupancy[black]

                    while attacks:
                        target_square = get_lsb1_index(attacks)
                        # promotion capture
                        if a7 <= start_square <= h7:
                            move_list.append(encode_move(start_square, target_square, piece, board_state.color, queen, 1, 0, 0, 0))
                            move_list.append(encode_move(start_square, target_square, piece, board_state.color, rook, 1, 0, 0, 0))
                            move_list.append(encode_move(start_square, target_square, piece, board_state.color, bishop, 1, 0, 0, 0))
                            move_list.append(encode_move(start_square, target_square, piece, board_state.color, knight, 1, 0, 0, 0))

                        else:
                            move_list.append(encode_move(start_square, target_square, piece, board_state.color, 0, 1, 0, 0, 0))

                        attacks = pop_bit(attacks, target_square)

                    if board_state.en_passant_square != 64:
                        en_passant_attacks = pawn_attacks[white][start_square] & np.ulonglong(1 << board_state.en_passant_square)

                        if en_passant_attacks:
                            target_en_passant = get_lsb1_index(en_passant_attacks)
                            move_list.append(encode_move(start_square, target_en_passant, piece, board_state.color, 0, 1, 0, 1, 0))

                    piece_bitboard = pop_bit(piece_bitboard, start_square)

            # castle moves
            if piece == king:
                # kingside castle
                if board_state.castle & wk:
                    if not get_bit(board_state.occupancy[both], f1) and not get_bit(board_state.occupancy[both], g1):
                        if not is_square_attacked(board_state, e1, black) and not is_square_attacked(board_state, f1, black):
                            move_list.append(encode_move(e1, g1, piece, board_state.color, 0, 0, 0, 0, 1))
                if board_state.castle & wq:
                    if not get_bit(board_state.occupancy[both], d1) and not get_bit(board_state.occupancy[both], c1) and not get_bit(board_state.occupancy[both], b1):
                        if not is_square_attacked(board_state, d1, black) and not is_square_attacked(board_state, e1, black):
                            move_list.append(encode_move(e1, c1, piece, board_state.color, 0, 0, 0, 0, 1))
        
        # black pieces
        if board_state.color == black:
            if piece == pawn:
                while piece_bitboard:
                    # black pawn move
                    start_square = get_lsb1_index(piece_bitboard)
                    target_square = start_square + 8

                    #quiet pawn move
                    if not (target_square > h1) and not get_bit(board_state.occupancy[both], target_square):

                      # promotion
                        if a2 <= start_square <= h2:
                            move_list.append(encode_move(start_square, target_square, piece, board_state.color, queen, 0, 0, 0, 0))
                            move_list.append(encode_move(start_square, target_square, piece, board_state.color, rook, 0, 0, 0, 0))
                            move_list.append(encode_move(start_square, target_square, piece, board_state.color, bishop, 0, 0, 0, 0))
                            move_list.append(encode_move(start_square, target_square, piece, board_state.color, knight, 0, 0, 0, 0))

                        else:
                            # pawn push
                            move_list.append(encode_move(start_square, target_square, piece, board_state.color, 0, 0, 0, 0, 0))

                            if a7 <= start_square <= h7 and not get_bit(board_state.occupancy[both], target_square + 8):
                                move_list.append(encode_move(start_square, target_square + 8, piece, board_state.color, 0, 0, 1, 0, 0))


                    attacks = pawn_attacks[black][start_square] & board_state.occupancy[white]

                    while attacks:
                        target_square = get_lsb1_index(attacks)
                        # promotion
                        if a2 <= start_square <= h2:
                            move_list.append(encode_move(start_square, target_square, piece, board_state.color, queen, 1, 0, 0, 0))
                            move_list.append(encode_move(start_square, target_square, piece, board_state.color, rook, 1, 0, 0, 0))
                            move_list.append(encode_move(start_square, target_square, piece, board_state.color, bishop, 1, 0, 0, 0))
                            move_list.append(encode_move(start_square, target_square, piece, board_state.color, knight, 1, 0, 0, 0))

                        else:
                            move_list.append(encode_move(start_square, target_square, piece, board_state.color, 0, 1, 0, 0, 0))

                        attacks = pop_bit(attacks, target_square)

                    if board_state.en_passant_square != 64:
                        en_passant_attacks = pawn_attacks[black][start_square] & np.ulonglong(1 << board_state.en_passant_square)
                        if en_passant_attacks:
                            target_en_passant = get_lsb1_index(en_passant_attacks)
                            move_list.append(encode_move(start_square, target_en_passant, piece, board_state.color, 0, 1, 0, 1, 0))
                    
                    piece_bitboard = pop_bit(piece_bitboard, start_square)

            # castle moves
            if piece == king:
                # kingside castle
                if board_state.castle & bk:
                    if not get_bit(board_state.occupancy[both], f8) and not get_bit(board_state.occupancy[both], g8):
                        if not is_square_attacked(board_state, e8, white) and not is_square_attacked(board_state, f8, white):
                            # print("castling move: e8g8")
                            move_list.append(encode_move(e8, g8, piece, board_state.color, 0, 0, 0, 0, 1))
                if board_state.castle & bq:
                    if not get_bit(board_state.occupancy[both], d8) and not get_bit(board_state.occupancy[both], c8) and not get_bit(board_state.occupancy[both], b8):
                        if not is_square_attacked(board_state, d8, white) and not is_square_attacked(board_state, e8, white):
                            # print("castling move: e8c8")
                            move_list.append(encode_move(e8, c8, piece, board_state.color, 0, 0, 0, 0, 1))
        
        if piece in range(1, 6):
            while piece_bitboard:
                start_square = get_lsb1_index(piece_bitboard)
                attacks = get_attacks(piece, start_square, board_state, board_state.color)

                while attacks:
                    target_square = get_lsb1_index(attacks)
                    if not get_bit(board_state.occupancy[opp_color], target_square):
                        move_list.append(encode_move(start_square, target_square, piece, board_state.color, 0, 0, 0, 0, 0))
                    else:
                        move_list.append(encode_move(start_square, target_square, piece, board_state.color, 0, 1, 0, 0, 0))

                    attacks = pop_bit(attacks, target_square)
                piece_bitboard = pop_bit(piece_bitboard, start_square)
    return move_list

def make_move(board_state_orig, move, only_captures = False):

    board_state = BoardState()
    board_state.pieces_bitboard = board_state_orig.pieces_bitboard.copy()
    board_state.occupancy = np.zeros(3, dtype=np.ulonglong)
    board_state.color = board_state_orig.color
    board_state.en_passant_square = board_state_orig.en_passant_square
    board_state.castle = board_state_orig.castle



    if not only_captures:

        start_square = get_move_source(move)
        target_square = get_move_target(move)
        piece = get_move_piece(move)
        color = int(get_move_color(move))
        opp_color = color ^ 1

        promoted_piece = get_move_promote_to(move)  
        capture_flag = get_move_capture(move)
        double_push_flag = get_move_double(move)
        enpassant_flag = get_move_enpassant(move)
        castling_flag = get_move_castling(move)

        # set bits in the piece bitboard
        board_state.pieces_bitboard[color][piece] = pop_bit(board_state.pieces_bitboard[color][piece], start_square)
        board_state.pieces_bitboard[color][piece] = set_bit(board_state.pieces_bitboard[color][piece], target_square)

        if capture_flag:
            for piece in Pieces:
                if get_bit(board_state.pieces_bitboard[opp_color][piece], target_square):
                    # pop bits in the piece bitboard
                    board_state.pieces_bitboard[opp_color][piece] = pop_bit(board_state.pieces_bitboard[opp_color][piece], target_square)
                    break

        if promoted_piece:
            # pop bits in the piece bitboard
            board_state.pieces_bitboard[color][pawn] = pop_bit(board_state.pieces_bitboard[color][pawn], target_square)


            # set bits in the piece bitboard
            board_state.pieces_bitboard[color][promoted_piece] = set_bit(board_state.pieces_bitboard[color][promoted_piece], target_square)

        if enpassant_flag: #capture en passant 
            if color==white: # black moved the pawn
               # pop bits in the piece bitboard
                board_state.pieces_bitboard[black][pawn] = pop_bit(board_state.pieces_bitboard[black][pawn], target_square + 8) 
            else:
               # pop bits in the piece bitboard
                board_state.pieces_bitboard[white][pawn] = pop_bit(board_state.pieces_bitboard[white][pawn], target_square - 8)

        board_state.en_passant_square = 64

        if double_push_flag:
            if color == white: 
                board_state.en_passant_square = target_square + 8 
            else:
               # pop bits in the piece bitboard
                board_state.en_passant_square = target_square - 8 

        if castling_flag:
            if target_square == g1:
                board_state.pieces_bitboard[color][rook] = pop_bit(board_state.pieces_bitboard[color][rook], h1)

                board_state.pieces_bitboard[color][rook] = set_bit(board_state.pieces_bitboard[color][rook], f1)

            elif target_square == c1:
                board_state.pieces_bitboard[color][rook] = pop_bit(board_state.pieces_bitboard[color][rook], a1)

                board_state.pieces_bitboard[color][rook] = set_bit(board_state.pieces_bitboard[color][rook], d1)

            elif target_square == g8:
                board_state.pieces_bitboard[color][rook] = pop_bit(board_state.pieces_bitboard[color][rook], h8)

                board_state.pieces_bitboard[color][rook] = set_bit(board_state.pieces_bitboard[color][rook], f8)

            elif target_square == c8:
                board_state.pieces_bitboard[color][rook] = pop_bit(board_state.pieces_bitboard[color][rook], a8)

                board_state.pieces_bitboard[color][rook] = set_bit(board_state.pieces_bitboard[color][rook], d8)


        # update castling rights
        board_state.castle &= castling_rights[start_square]
        board_state.castle &= castling_rights[target_square]

        # update occ
        for c in [white, black]:
            for bb in board_state.pieces_bitboard[c]:
                board_state.occupancy[c] |= bb
            board_state.occupancy[both] |= board_state.occupancy[c]

        board_state.color = opp_color

        if not is_square_attacked(board_state, get_lsb1_index(board_state.pieces_bitboard[color][king]), opp_color):
            return board_state

    else:
        if get_move_capture(move):
            return make_move(board_state, move, False)
        return None

    return None

def generate_legal_moves(pos):
    """only for debugging purposes"""
    return [move for move in generate_pseudo_legal_moves(pos) if make_move(pos, move)]
