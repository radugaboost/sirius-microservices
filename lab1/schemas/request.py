from pydantic import BaseModel


class DoRequest(BaseModel):
    number: int
