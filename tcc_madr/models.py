from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class Conta:
    __tablename__ = 'conta'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    senha: Mapped[str]


@table_registry.mapped_as_dataclass
class Romancistas:
    __tablename__ = 'romancistas'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    nome: Mapped[str] = mapped_column(unique=True)

    livros: Mapped[list['Livro']] = relationship(
        back_populates='autoria',
        cascade='all, delete-orphan',
        default_factory=list,  # Define uma lista vazia como valor padrão
    )


@table_registry.mapped_as_dataclass
class Livro:
    __tablename__ = 'livro'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    ano: Mapped[int]
    titulo: Mapped[str] = mapped_column(unique=True)
    romancista_id: Mapped[int] = mapped_column(ForeignKey('romancistas.id'))
    autoria: Mapped[Romancistas] = relationship(
        init=False, back_populates='livros'
    )
