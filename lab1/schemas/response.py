from pydantic import BaseModel


class DefaultResponse(BaseModel):
    result: float
