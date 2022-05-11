from constants import Piece, Color, algebraic_square_map, square_to_coordinates
from tables import bishop_attacks, rook_attacks, pawn_attacks, knight_attacks, king_attacks
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
        opponent_color = ~board.color

        # white pawns & castling
        if board.color == Color.WHITE:
            if piece == piece.PAWN:
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
                            print("pawn push: ", square_to_coordinates[start_square], square_to_coordinates[target_square-8])

                    piece_bitboard = pop_bit(piece_bitboard, start_square)

    return move_list