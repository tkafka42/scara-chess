import chess

BOX = "box"
RESERVE = "reserve"


def move_enpassant(board, move):
    takenpiecerank = 0
    takenpiecefile = chess.square_file(move.to_square)

    if board.turn == chess.WHITE:
        takenpiecerank = chess.square_rank(move.to_square) - 1
    else:
        takenpiecerank = chess.square_rank(move.to_square) + 1

    captured = chess.square(takenpiecefile, takenpiecerank)
    return [(captured, BOX), (move.from_square, move.to_square)]


def move_castling(board, move):
    if board.turn == chess.WHITE:
        if board.is_kingside_castling(move):
            rook_from, rook_to = chess.H1, chess.F1
        else:
            rook_from, rook_to = chess.A1, chess.D1
    else:
        if board.is_kingside_castling(move):
            rook_from, rook_to = chess.H8, chess.F8
        else:
            rook_from, rook_to = chess.A8, chess.D8

    return [(move.from_square, move.to_square), (rook_from, rook_to)]


if __name__ == "__main__":
    board = chess.Board()
    for san in ["e4", "a6", "e5", "d5"]:
        board.push_san(san)
    move = chess.Move.from_uci("e5d6")
    for frm, to in move_enpassant(board, move):
        print(
            frm if frm in (BOX, RESERVE) else chess.square_name(frm),
            "->",
            to if to in (BOX, RESERVE) else chess.square_name(to),
        )
    board = chess.Board("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1")
    for uci in ["e1g1", "e1c1"]:
        print(uci, move_castling(board, chess.Move.from_uci(uci)))
