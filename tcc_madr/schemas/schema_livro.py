from pydantic import BaseModel, ConfigDict, field_validator

from tcc_madr.utils import sanitize_input


class LivroSchema(BaseModel):
    ano: int
    titulo: str
    romancista_id: int

    @field_validator('titulo')
    def sanitize_username(cls, text: str):
        return sanitize_input(text)


class LivroPublic(BaseModel):
    id: int
    ano: int
    titulo: str
    romancista_id: int
    model_config = ConfigDict(from_attributes=True)


class LivroList(BaseModel):
    livros: list[LivroPublic]


class LivroUpdate(BaseModel):
    titulo: str | None = None
    ano: int | None = None
    romancista_id: int | None = None

    @field_validator('titulo')
    def sanitize_username(cls, text: str):
        return sanitize_input(text)
