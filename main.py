# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("src.app:app", port=8000)

import chess
import chess.engine
import chess.polyglot

# Initialize board from FEN notation
fen = "4kb1r/3rn1pp/4Qp2/1B2p3/8/2NPB2P/Pq3P1P/R5K1 b k - 4 18"
board = chess.Board(fen)

# 1. Material Balance
material_count = {
    "White": sum(1 for piece in board.pieces(chess.PAWN, chess.WHITE)) +
             sum(3 for piece in board.pieces(chess.KNIGHT, chess.WHITE)) +
             sum(3 for piece in board.pieces(chess.BISHOP, chess.WHITE)) +
             sum(5 for piece in board.pieces(chess.ROOK, chess.WHITE)) +
             sum(9 for piece in board.pieces(chess.QUEEN, chess.WHITE)),
    "Black": sum(1 for piece in board.pieces(chess.PAWN, chess.BLACK)) +
             sum(3 for piece in board.pieces(chess.KNIGHT, chess.BLACK)) +
             sum(3 for piece in board.pieces(chess.BISHOP, chess.BLACK)) +
             sum(5 for piece in board.pieces(chess.ROOK, chess.BLACK)) +
             sum(9 for piece in board.pieces(chess.QUEEN, chess.BLACK))
}

# 2. King Safety
white_king_safety = board.is_check() if board.turn == chess.WHITE else None
black_king_safety = board.is_check() if board.turn == chess.BLACK else None

# 3. Piece Activity
# active_pieces = {
#     "White": [str(piece) for piece in board.pieces(chess.PIECE_TYPES, chess.WHITE)],
#     "Black": [str(piece) for piece in board.pieces(chess.PIECE_TYPES, chess.BLACK)]
# }

# 4. Pawn Structure
pawn_structure = {
    "White": list(board.pieces(chess.PAWN, chess.WHITE)),
    "Black": list(board.pieces(chess.PAWN, chess.BLACK))
}

# 5. Control of Key Squares (e.g., central squares)
center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
control = {
    "White": [square for square in center_squares if board.attackers(chess.WHITE, square)],
    "Black": [square for square in center_squares if board.attackers(chess.BLACK, square)]
}