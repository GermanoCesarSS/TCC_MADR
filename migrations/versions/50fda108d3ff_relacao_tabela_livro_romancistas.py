"""relacao tabela livro romancistas

Revision ID: 50fda108d3ff
Revises: 80dc57b3dd72
Create Date: 2024-12-05 15:44:20.974606

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '50fda108d3ff'
down_revision: Union[str, None] = '80dc57b3dd72'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
      # Renomear a tabela existente
    op.rename_table('livro', 'livro_old')

    # Criar a nova tabela com a chave estrangeira correta
    op.create_table(
        'livro',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('ano', sa.Integer(), nullable=False),
        sa.Column('titulo', sa.String(), unique=True, nullable=False),
        sa.Column('romancista_id', sa.Integer(), sa.ForeignKey('romancistas.id', ondelete='CASCADE'), nullable=False)
    )

    # Copiar os dados da tabela antiga para a nova
    op.execute("""
        INSERT INTO livro (id, ano, titulo, romancista_id)
        SELECT id, ano, titulo, romancista_id
        FROM livro_old
    """)

    # Remover a tabela antiga
    op.drop_table('livro_old')


def downgrade() -> None:
    # Reverter o processo (recriar a tabela antiga)
    op.rename_table('livro', 'livro_new')

    op.create_table(
        'livro',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('ano', sa.Integer(), nullable=False),
        sa.Column('titulo', sa.String(), unique=True, nullable=False),
        sa.Column('romancista_id', sa.Integer(), nullable=False)  # Sem chave estrangeira
    )

    op.execute("""
        INSERT INTO livro (id, ano, titulo, romancista_id)
        SELECT id, ano, titulo, romancista_id
        FROM livro_new
    """)

    op.drop_table('livro_new')
