from move import encode_move, get_move_uci
from generate_moves import generate_pseudo_legal_moves, make_move, generate_legal_moves
from board_state import BoardState
import chess
import sys


def perft_main(board, depth):
	if depth == 0:
		return 1


	moves = generate_legal_moves(board)
	nodes = 0
	for move in moves:
		new_board = make_move(board, move)
		if new_board is not None:
			n = perft_main(new_board, depth - 1)
			nodes += n
	return nodes

def debug_perft(board, depth, b, print_info=False):
    """perft test with python-chess in parallel to narrow down the bugs"""
    if depth == 0:
        return 1
    count = 0
    moves = generate_legal_moves(board)
    PC_moves = set(m.uci() for m in b.legal_moves)
    JACE_moves = set(get_move_uci(m) for m in moves)
    if PC_moves != JACE_moves:
        print("Moves played:", [m.uci() for m in b.move_stack])
        print("In this position:", b.fen())
        # problem_board = BoardState()
        # problem_board.set_fen(b.fen())
        print(board)
        if PC_moves - JACE_moves:
            print("JACE does not see:", PC_moves - JACE_moves)
            print(JACE_moves)
        else:
            print("JACE thinks she can play:", JACE_moves - PC_moves)
        sys.exit()

    for m in moves:
        b.push_uci(get_move_uci(m))
        c = debug_perft(make_move(board, m), depth - 1, b)
        count += c
        b.pop()
        if print_info:
            print(f"move: {get_move_uci(m)}     nodes: {c}")
    return count