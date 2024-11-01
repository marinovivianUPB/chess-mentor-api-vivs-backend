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

@app.post("/state")
def calculate_board_state(req: ApiRequest, agent: ReActAgent = Depends(get_agent)):
    prompt = f"""
        Given this position in the chessboard in FEN notation: {req.fen}.
        Can you provide an analisys of the current board state, take on account the following aspects: 
        - The amount of material for both sides
        - The pieces that are active
        - The pieces that are delivering check
        - The pieces that are under attack for both sides
        - The pieces that are attacking for both sides
        - The pieces that are pinned
        - The pieces that are defending other pieces
        - The pieces that are undefended
        - The pawn structure

        Once you have this information, please explain it as a chess master that is teaching me how to improve my games.
        I want to understand the board state and how to take advantage of it.
        Please tell me the strategy I should follow to win the game.

        Summarize your answer in a small list containing the main insights of the game
        and each item should be at most a paragraph, I only need information that is relevant to my chess learning process.
        Use this language for your answer: {req.language}.
    """
    response = agent.query(prompt)
    return ApiResponse(
        message="Board state generated succesfully",
        agent_response=str(response),
    )

@app.post("/analysis")
def analyze_match(req: ApiRequest, agent: ReActAgent = Depends(get_agent)):
    return ApiResponse(
        message="Match analysis generated succesfully",
    )

@app.post("/chat")
def chat(query: str):
    return ApiResponse(
        message="Chat response generated succesfully",
        data={"response": "I am your chess mentor"}
    )
