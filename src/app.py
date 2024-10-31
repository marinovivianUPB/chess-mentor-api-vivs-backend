from fastapi import FastAPI, Depends
from llama_index.core.agent import ReActAgent
from functools import cache

from src.models import ApiRequest, ApiResponse
from src.agent import ChessAgent
from src.tools import get_best_move
from fastapi.middleware.cors import CORSMiddleware


@cache
def get_agent() -> ReActAgent:
    return ChessAgent().get_agent()


app = FastAPI(title="Chess Mentor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def get_health():
    return "Server is running"


@app.post("/best-move")
def calculate_best_move(req: ApiRequest, agent: ReActAgent = Depends(get_agent)):
    best_move=get_best_move(fen=req.fen)
    prompt = f"""
        Given this position in the chessboard in FEN notation: {req.fen}.
        Can you provide the next best move I can do, 
        then explain it as a chess master that is teaching me how to improve my games.
        Summarize your answer in one paragraph in the following language: {req.language}.
    """
    response = agent.query(prompt)
    return ApiResponse(
        message="Best move calculated succesfully",
        agent_response=str(response),
        # data=best_move
    )


@app.post("/chat")
def chat(query: str):
    return ApiResponse(
        message="Chat response generated succesfully",
        data={"response": "I am your chess mentor"}
    )
