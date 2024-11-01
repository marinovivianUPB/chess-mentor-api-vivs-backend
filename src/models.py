from pydantic import BaseModel

class Move(BaseModel):
    color: int
    from_square: str
    to_square: str

class ApiRequest(BaseModel):
    fen: str
    language: str = 'en'
    next_move: Move | None = None
    history: list[Move] | None = None


class MoveAnalysis(BaseModel):
    centipawn_score: int
    win_chance: float
    comment: str


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


class ApiResponse(BaseModel):
    message: str
    agent_response: str
    data: Move | BoardAnalysis | MoveAnalysis | dict | None = None
