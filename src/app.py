from fastapi import FastAPI, Depends
from llama_index.core.agent import ReActAgent
from functools import cache

from src.models import ApiResponse
from src.agent import ChessAgent
from src.tools import get_best_move


@cache
def get_agent() -> ReActAgent:
    return ChessAgent().get_agent()


app = FastAPI(title="Chess Mentor API")


@app.get("/")
def get_health():
    return "Server is running"


@app.post("/best-move")
def calculate_best_move(fen: str, language: str = 'en', agent: ReActAgent = Depends(get_agent)):
    best_move=get_best_move(fen=fen)
    prompt = f"""
        Given this position in the chessboard in FEN notation: {fen}.
        Can you provide the next best move I can do, 
        then explain it as a chess master that is teaching me how to improve my games.
        Summarize your answer in one paragraph in the following language: {language}.
    """
    response = agent.query(prompt)
    return ApiResponse(
        message="Best move calculated succesfully",
        data={"response": str(response), "best_move": best_move}
    )


@app.post("/chat")
def chat(query: str):
    return ApiResponse(
        message="Chat response generated succesfully",
        data={"response": "I am your chess mentor"}
    )
