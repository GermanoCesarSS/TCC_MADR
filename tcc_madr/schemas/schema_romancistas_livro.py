from pydantic import BaseModel, ConfigDict


class RomancistasLivrosViewPublic(BaseModel):
    romancista_id: int
    romancista_nome: str
    livro_id: int | None = None
    livro_titulo: str | None = None
    livro_ano: int | None = None
    model_config = ConfigDict(from_attributes=True)


class RomancistasLivrosViewList(BaseModel):
    romancistas_livro_view: list[RomancistasLivrosViewPublic]
