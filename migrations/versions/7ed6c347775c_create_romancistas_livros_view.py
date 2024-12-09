"""create romancistas_livros view

Revision ID: 7ed6c347775c
Revises: 50fda108d3ff
Create Date: 2024-12-08 22:57:39.281568

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7ed6c347775c'
down_revision: Union[str, None] = '50fda108d3ff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
     # Criar a View 'romancistas_livros'
    op.execute("""
        CREATE VIEW romancistas_livros AS
        SELECT 
            r.id AS romancista_id,
            r.nome AS romancista_nome,
            l.id AS livro_id,
            l.titulo AS livro_titulo,
            l.ano AS livro_ano
        FROM 
            romancistas r
        LEFT JOIN 
            livro l ON r.id = l.romancista_id
    """)


def downgrade() -> None:
    # Remover a View 'romancistas_livros'
    op.execute("DROP VIEW IF EXISTS romancistas_livros")
