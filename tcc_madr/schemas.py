from pydantic import BaseModel


class Message(BaseModel):
    mensagem: str
