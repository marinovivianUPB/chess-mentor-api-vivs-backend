import requests
from llama_index.core.tools import FunctionTool

from src.rags import ChessExpertRAG
from src.prompts import chess_guide_qa_tpl, chess_expert_description
from llama_index.core.tools import QueryEngineTool, FunctionTool, ToolMetadata

from src.config import get_agent_settings

SETTINGS = get_agent_settings()


chess_expert_tool = QueryEngineTool(
    query_engine=ChessExpertRAG(
        store_path=SETTINGS.store_path,
        data_dir=SETTINGS.docs_path,
        qa_prompt_tpl=chess_guide_qa_tpl,
    ).get_query_engine(),
    metadata=ToolMetadata(
        name="chess_expert", description=chess_expert_description, return_direct=False
    ),
)


def get_best_move(fen: str) -> dict:
    """
    Get the best move based on the current board state.
    Args:
        - fen (str): FEN notation of the current board state.
    Returns:
        - dict: The best move to make and addtional information.
    """
    response = requests.post("https://chess-api.com/v1", {"fen": fen})
    return response.json()

best_move_tool = FunctionTool.from_defaults(fn=get_best_move, return_direct=False)
