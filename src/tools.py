import requests
from llama_index.core.tools import FunctionTool
from functools import cache
import chess


@cache
def get_stockfish_analysis(fen: str) -> dict:
    print(f"Getting best move for FEN: {fen}")
    response = requests.post("https://chess-api.com/v1", {"fen": fen})
    return response.json()

def get_best_move(fen: str) -> dict:
    """
    Get the best move based on the current board state.
    Args:
        - fen (str): FEN notation of the current board state.
    Returns:
        - dict: The best move to make and addtional information.
    """
    print(f"Getting best move for FEN: {fen}")
    
    piece_types = {
        "p": "pawn",
        "n": "knight",
        "b": "bishop",
        "r": "rook",
        "q": "queen",
        "k": "king"
    }

    move_types = {
        "n": "non-capture",
        "b": "pawn push of two squares",
        "e": "en passant capture",
        "c": "standard capture",
        "p": "promotion",
        "k": "kingside castling",
        "q": "queenside castling"
    }

    analysis = get_stockfish_analysis(fen)

    text = analysis.get("text")
    move = analysis.get("move")

    from_square = analysis.get("from")
    to_square = analysis.get("to")

    piece = analysis.get("piece")
    captured = analysis.get("captured")
    promotion = analysis.get("promotion")

    flags = analysis.get("flags")
    move_type = [move_types[flag] for flag in list(flags)]

    return {
        "text": text,
        "move": move,
        "from_square": from_square,
        "to_square": to_square,
        "piece_type": piece_types[piece],
        "move_type": move_type,
        "captured": piece_types[captured] if captured in piece_types else None,
        "promotion": piece_types[promotion] if promotion in piece_types else None,
    }


def analize_position(fen: str) -> dict:
    """
    Analize the current board state.
    Args:
        - fen (str): FEN notation of the current board state.
    Returns:
        - dict: The analysis of the board state.
    """
    print(f"Analizing position for FEN: {fen}")

    analysis = get_stockfish_analysis(fen)
    centipawn_score = analysis["centipawns"]
    win_chance = analysis["winChance"]
    
    board = chess.Board(fen)
    pieces = board.piece_map()

    checkers = board.checkers()

    # Black attackers
    black_attackers = []
    for square in chess.SQUARES:
        if square in pieces:
            if pieces[square].color == chess.WHITE:
                attackers = board.attackers(chess.BLACK, square)
                black_attackers.append(attackers)
    
    # White attackers
    white_attackers = []
    for square in chess.SQUARES:
        if square in pieces:
            if pieces[square].color == chess.WHITE:
                attackers = board.attackers(chess.BLACK, square)
                white_attackers.append(attackers)

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

    white_king_safety = board.is_check() if board.turn == chess.WHITE else None
    black_king_safety = board.is_check() if board.turn == chess.BLACK else None

    pawn_structure = {
        "White": list(board.pieces(chess.PAWN, chess.WHITE)),
        "Black": list(board.pieces(chess.PAWN, chess.BLACK))
    }

    center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
    control = {
        "White": [square for square in center_squares if board.attackers(chess.WHITE, square)],
        "Black": [square for square in center_squares if board.attackers(chess.BLACK, square)]
    }
    
    return {
        "centipawn_score": centipawn_score,
        "win_chance": win_chance,
        "checkers": checkers,
        "black_attackers": black_attackers,
        "white_attackers": white_attackers,
        "material_count": material_count,
        "white_king_safety": white_king_safety,
        "black_king_safety": black_king_safety,
        "pawn_structure": pawn_structure,
        "control": control
    }

def analize_move(fen: str, move: str) -> dict:
    """
    Analize the move made in the current board state.
    Args:
        - fen (str): FEN notation of the current board state.
        - move (str): The move made.
    Returns:
        - dict: The analysis of the move made.
    """
    print(f"Analizing move {move} from FEN: {fen}")
    
    prev_analysis = analize_position(fen)
    board = chess.Board(fen)
    board.push_san(move)
    new_fen = board.fen()
    new_analysis = analize_position(new_fen)

    centipawn_score_diff = new_analysis["centipawn_score"] - prev_analysis["centipawn_score"]
    win_chance_diff = new_analysis["win_chance"] - prev_analysis["win_chance"]

    material_count_diff = {
        "White": new_analysis["material_count"]["White"] - prev_analysis["material_count"]["White"],
        "Black": new_analysis["material_count"]["Black"] - prev_analysis["material_count"]["Black"]
    }

    return {
        "centipawn_score_diff": centipawn_score_diff,
        "win_chance_diff": win_chance_diff,
        "material_count_diff": material_count_diff
    }


best_move_tool = FunctionTool.from_defaults(fn=get_best_move, return_direct=False)
analize_position_tool = FunctionTool.from_defaults(fn=analize_position, return_direct=False)
analize_move_tool = FunctionTool.from_defaults(fn=analize_move, return_direct=False)