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


def move_promotion(board, move):
    actions = []
    if board.is_capture(move):
        actions.append((move.to_square, BOX))
    actions.append((move.from_square, BOX))
    actions.append((RESERVE, move.to_square))
    return actions


def move_capture(board, move):
    return [(move.to_square, BOX), (move.from_square, move.to_square)]


def move_classic(board, move):
    return [(move.from_square, move.to_square)]


def move_to_actions(board, move):
    if board.is_en_passant(move):
        return move_enpassant(board, move)
    elif board.is_castling(move):
        return move_castling(board, move)
    elif move.promotion:
        return move_promotion(board, move)
    elif board.is_capture(move):
        return move_capture(board, move)
    else:
        return move_classic(board, move)


if __name__ == "__main__":

    def name(location):
        return location if location in (BOX, RESERVE) else chess.square_name(location)

    tests = [
        (None, [], "e2e4", [("e2", "e4")]),
        (None, ["e4", "d5"], "e4d5", [("d5", "box"), ("e4", "d5")]),
        (None, ["e4", "a6", "e5", "d5"], "e5d6", [("d5", "box"), ("e5", "d6")]),
        (
            "r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1",
            [],
            "e1g1",
            [("e1", "g1"), ("h1", "f1")],
        ),
        (
            "r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1",
            [],
            "e1c1",
            [("e1", "c1"), ("a1", "d1")],
        ),
        (
            "8/P7/8/8/8/8/8/k6K w - - 0 1",
            [],
            "a7a8q",
            [("a7", "box"), ("reserve", "a8")],
        ),
        (
            "1n6/P7/8/8/8/8/8/k6K w - - 0 1",
            [],
            "a7b8q",
            [("b8", "box"), ("a7", "box"), ("reserve", "b8")],
        ),
    ]

    ok = 0
    for fen, before, uci, expected in tests:
        board = chess.Board(fen) if fen else chess.Board()
        for san in before:
            board.push_san(san)
        actions = move_to_actions(board, chess.Move.from_uci(uci))
        result = [(name(a), name(b)) for a, b in actions]
        if result == expected:
            ok += 1
        else:
            print(f"{uci}: got {result}, expected {expected}")
    print(f"{ok}/{len(tests)} ok")
