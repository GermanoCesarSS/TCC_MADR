from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

from tcc_madr.utils import sanitize_input


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
    model_config = ConfigDict(from_attributes=True)


class ContaList(BaseModel):
    contas: list[ContaPublic]


class ContaUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    senha: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str
