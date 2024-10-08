"""Initial migration

Revision ID: b360a0fe8776
Revises: 
Create Date: 2024-09-23 07:49:33.890937

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b360a0fe8776'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('puzzles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('puzzle_type', sa.String(), nullable=False),
    sa.Column('size_x', sa.Integer(), nullable=False),
    sa.Column('size_y', sa.Integer(), nullable=False),
    sa.Column('difficulty', sa.Integer(), nullable=False),
    sa.Column('puzzle_data', sa.Text(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('size_x', 'size_y', 'difficulty', 'puzzle_data')
    )
    op.create_index(op.f('ix_puzzles_id'), 'puzzles', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_puzzles_id'), table_name='puzzles')
    op.drop_table('puzzles')
    # ### end Alembic commands ###
