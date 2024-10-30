from pydantic import BaseModel
import chess

class ApiResponse(BaseModel):
    message: str
    data: dict | list | None = None

class BoardAnalysis(BaseModel):
    checkers: list
    black_attackers: list
    white_attackers: list

class PieceState(BaseModel):
    id: int
    type: str
    color: str
    square: str
    attacked_by: list
    attacking: list