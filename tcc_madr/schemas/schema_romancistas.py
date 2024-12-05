from pydantic import BaseModel, ConfigDict, field_validator

from tcc_madr.utils import sanitize_input_up


class RomancistasSchema(BaseModel):
    nome: str

    @field_validator('nome')
    def sanitize_username(cls, text: str):
        return sanitize_input_up(text)


class RomancistasPublic(BaseModel):
    id: int
    nome: str
    model_config = ConfigDict(from_attributes=True)


class RomancistasUpdata(BaseModel):
    nome: str | None = None

    @field_validator('nome')
    def sanitize_username(cls, text: str):
        return sanitize_input_up(text)


class RomancistasList(BaseModel):
    romancistas: list[RomancistasPublic]
