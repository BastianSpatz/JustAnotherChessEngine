from generate_moves import generate_pseudo_legal_moves, make_move

def perft_main(board, depth):
	if depth == 0:
		return 1


	moves = generate_pseudo_legal_moves(board)
	nodes = 0
	for move in moves:
		new_board = make_move(board, move)
		if new_board is not None:
			n = perft_main(new_board, depth - 1)
			nodes += n
	return nodes
