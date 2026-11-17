import chess

BOX = "box"
RESERVE = "reserve"


def move_enpassant(board, move):
    mvFrom = move.from_square
    mvTo = move.to_square
    takenpiecerank = 0
    takenpiecefile = chess.square_file(move.to_square)

    if board.turn == chess.WHITE:
        takenpiecerank = chess.square_rank(move.to_square) - 1
    else:
        takenpiecerank = chess.square_rank(move.to_square) + 1

    captured = chess.square(takenpiecefile, takenpiecerank)
    return [(captured, BOX), (move.from_square, move.to_square)]


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
