from pydantic import BaseModel, EmailStr, field_validator

from tcc_madr.utils import sanitize_input


class Message(BaseModel):
    mensagem: str


class ContaSchema(BaseModel):
    username: str
    email: EmailStr
    senha: str

    @field_validator('username')
    def sanitize_username(cls, text: str):
        return sanitize_input(text)


class ContaPublic(BaseModel):
    id: int
    email: EmailStr
    username: str
