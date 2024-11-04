from fastapi import FastAPI, Depends
from llama_index.core.agent import ReActAgent
from functools import cache

from src.models import ApiResponse, ChatApiRequest
from src.agent import MagnusAgent

from fastapi.middleware.cors import CORSMiddleware


@cache
def get_chat_agent() -> ReActAgent:
    return MagnusAgent().get_agent()


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
def calculate_best_move(fen: str, language: str = 'en', agent: ReActAgent = Depends(get_chat_agent)):
    prompt = f"""
        Given this position in the chessboard in FEN notation: {fen}.
        Can you provide the next best move I can do, 
        then explain it as a chess master that is teaching me how to improve my games.
        Summarize your answer in one paragraph in the following language: {language}.
    """
    response = agent.query(prompt)
    return ApiResponse(
        message="Best move calculated succesfully",
        data={"response": str(response)}
    )


@app.post("/chat")
def chat(req: ChatApiRequest, agent: ReActAgent = Depends(get_chat_agent)):
    response = agent.chat(req.message)
    return ApiResponse(
        message="Chat response generated succesfully",
        data={"response": response}
    )


