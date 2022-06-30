from board_state import BoardState, print_board_state, set_fen
from constants import STARTING_FEN
from generate_moves import generate_pseudo_legal_moves, make_move
from perft import perft
import time

board = set_fen("r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq -")

for i in range(5):
	start = time.time() #start time
	nodes = perft(board, i)
	end = time.time()
	print("perft(" + str(i) + ") - " + str(end-start))