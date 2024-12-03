from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class Conta:
    __tablename__ = 'conta'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    senha: Mapped[str]


@table_registry.mapped_as_dataclass
class Livro:
    __tablename__ = 'livro'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    ano: Mapped[str]
    titulo: Mapped[str] = mapped_column(unique=True)
    romancista_id: Mapped[int]
