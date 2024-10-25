import requests
from llama_index.core.tools import FunctionTool
from functools import cache

@cache
def get_best_move(fen: str) -> dict:
    """
    Get the best move based on the current board state.
    Args:
        - fen (str): FEN notation of the current board state.
    Returns:
        - dict: The best move to make and addtional information.
    """
    print(f"Getting best move for FEN: {fen}")
    response = requests.post("https://chess-api.com/v1", {"fen": fen})
    return response.json()

best_move_tool = FunctionTool.from_defaults(fn=get_best_move, return_direct=False)
