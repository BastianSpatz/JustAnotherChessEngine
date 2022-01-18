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
        self.target_square = target_square,  
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

    def get_move_side(self):
        return bool(self.binary_move & 0x8000)

    def get_move_promote_to(self):
        return (self.binary_move & 0xf0000) >> 16

    def get_move_capture(self):
        return bool(self.binary_move & 0x100000)

    def get_move_double(self):
        return bool(self.binary_move & 0x200000)

    def get_move_enpas(self):
        return bool(self.binary_move & 0x400000)

    def get_move_castling(self):
        return bool(self.binary_move & 0x800000)