from constants import square_to_coordinates, PIECE_SYMBOLS, UNICODE_PIECE_SYMBOLS

def encode_move(start_square, target_square, piece, color, promoted_piece, capture_flag, double_push_flag, enpassant_flag, castling_flag):
    return start_square \
            | target_square << 6 \
            | piece << 12 \
            | color << 15 \
            | promoted_piece << 16 \
            | capture_flag << 20 \
            | double_push_flag << 21 \
            | enpassant_flag << 22 \
            | castling_flag << 23

def get_move_source(move):
    return move & 0x3f

def get_move_target(move):
    return (move & 0xfc0) >> 6

def get_move_piece(move):
    return (move & 0x7000) >> 12

def get_move_color(move):
    return bool(move & 0x8000)

def get_move_promote_to(move):
    return (move & 0xf0000) >> 16

def get_move_capture(move):
    return bool(move & 0x100000)

def get_move_double(move):
    return bool(move & 0x200000)

def get_move_enpassant(move):
    return bool(move & 0x400000)

def get_move_castling(move):
    return bool(move & 0x800000)

def get_move_uci(move):
    """get the uci string of a move"""
    source = str(square_to_coordinates[get_move_source(move)]) 
    target = str(square_to_coordinates[get_move_target(move)])
    promoted_piece = PIECE_SYMBOLS[get_move_promote_to(move) + 6] if get_move_promote_to(move) else ""
    return source + target + promoted_piece  

def uci_move_encoding(uci_move):
    """encode uci string to move"""
    start_square = algebraic_square_map[uci_move[0:2]]
    target_square = algebraic_square_map[uci_move[2:4]]

    if len(uci_move) > 4:
        promoted_piece_str = uci_move[-1] 
        promoted_piece, _ = piece_from_symbol(promoted_piece_str)
    else:
        promoted_piece = 0

    for p, bb in enumerate(board.pieces_bitboard[board.color]):
        if get_bit(bb, start_square):
            piece = p
            break
    color = board.color
    opp_color = color^1


    for bb in board.pieces_bitboard[opp_color]:
        if get_bit(bb, target_square):
            capture_flag=1
            break
        else:
            capture_flag=0

    if piece == pawn and abs(target_square - start_square)==16:
        double_push_flag = 1
    else:
        double_push_flag = 0

    if piece == pawn and target_square==board.en_passant_square:
        enpassant_flag = 1
    else:
        enpassant_flag = 0

    castling_flag = 0
    if piece == king:
        # kingside castle
        if board.color == white:
            if board.castle & wk and target_square==algebraic_square_map["g1"]:
                castling_flag = 1 
            elif board.castle & wq and target_square==algebraic_square_map["c1"]:
                castling_flag = 1 
            else:
                castling_flag = 0

        if board.color == black:
            if board.castle & bk and target_square==algebraic_square_map["g8"]:
                castling_flag = 1 
            elif board.castle & bq and target_square==algebraic_square_map["c8"]:
                castling_flag = 1 
            else:
                castling_flag = 0

    return encode_move(start_square, target_square, piece, color, promoted_piece, capture_flag, double_push_flag, enpassant_flag, castling_flag)


def print_move(move):
    start_square = get_move_source(move)
    target_square = get_move_target(move)
    color = get_move_color(move)
    piece = get_move_piece(move)
    promoted_piece = get_move_promote_to(move)
    if promoted_piece != 0: 
        prom_piece = PIECE_SYMBOLS[promoted_piece + color*6] 
    else:
        prom_piece = ""
    return UNICODE_PIECE_SYMBOLS[PIECE_SYMBOLS[piece + color*6]] + square_to_coordinates[start_square] + "-" + square_to_coordinates[target_square] + prom_piece