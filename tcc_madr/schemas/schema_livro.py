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
    contas: list[LivroPublic]
