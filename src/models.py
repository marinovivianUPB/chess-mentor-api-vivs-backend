from pydantic import BaseModel

class ApiResponse(BaseModel):
    message: str
    data: dict | list | None = None

class ChatApiRequest(BaseModel):
    message: str
