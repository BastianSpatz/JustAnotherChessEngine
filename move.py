from constants import square_to_coordinates, PIECE_SYMBOLS, UNICODE_PIECE_SYMBOLS

class Move():
    def __init__(self, 
                    start_square, 
                    target_square, 
                    piece, 
                    color, 
                    promoted_piece, 
                    capture_flag, 
                    double_push_flag,
                    enpassant_flag,
                    castling_flag):

        self.start_square = start_square
        self.target_square = target_square
        self.piece = piece  
        self.color = color  
        self.promoted_piece = promoted_piece  
        self.capture_flag = capture_flag  
        self.double_push_flag = double_push_flag
        self.enpassant_flag = enpassant_flag
        self.castling_flag = castling_flag

        self.binary_move = self.encode_move()

    def encode_move(self):
        return self.start_square \
                | self.target_square << 6 \
                | self.piece << 12 \
                | self.color << 15 \
                | self.promoted_piece << 16 \
                | self.capture_flag << 20 \
                | self.double_push_flag << 21 \
                | self.enpassant_flag << 22 \
                | self.castling_flag << 23

    def get_move_source(self):
        return self.binary_move & 0x3f

    def get_move_target(self):
        return (self.binary_move & 0xfc0) >> 6

    def get_move_piece(self):
        return (self.binary_move & 0x7000) >> 12

    def get_move_color(self):
        return bool(self.binary_move & 0x8000)

    def get_move_promote_to(self):
        return (self.binary_move & 0xf0000) >> 16

    def get_move_capture(self):
        return bool(self.binary_move & 0x100000)

    def get_move_double(self):
        return bool(self.binary_move & 0x200000)

    def get_move_enpassant(self):
        return bool(self.binary_move & 0x400000)

    def get_move_castling(self):
        return bool(self.binary_move & 0x800000)    

    def __str__(self):
        start_square = self.get_move_source()
        target_square = self.get_move_target()
        color = self.get_move_color()
        piece = self.get_move_piece()
        promoted_piece = self.get_move_promote_to()
        if promoted_piece != 0: 
            prom_piece = PIECE_SYMBOLS[promoted_piece + color*6] 
        else:
            prom_piece = ""
        return UNICODE_PIECE_SYMBOLS[PIECE_SYMBOLS[piece + color*6]] + square_to_coordinates[start_square] + "-" + square_to_coordinates[target_square] + prom_piece