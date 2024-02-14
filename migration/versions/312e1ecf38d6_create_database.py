"""Create database

Revision ID: 312e1ecf38d6
Revises: 
Create Date: 2024-02-14 20:15:15.590074

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '312e1ecf38d6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('shift_tasks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('closing_status', sa.Boolean(), nullable=False),
    sa.Column('closed_at', sa.Date(), nullable=True),
    sa.Column('submission_task_shift', sa.String(length=50), nullable=False),
    sa.Column('line', sa.String(length=10), nullable=False),
    sa.Column('shift', sa.String(length=10), nullable=False),
    sa.Column('brigade', sa.String(length=50), nullable=False),
    sa.Column('batch_number', sa.Integer(), nullable=False),
    sa.Column('batch_date', sa.Date(), nullable=False),
    sa.Column('nomenclature', sa.String(length=100), nullable=False),
    sa.Column('code', sa.String(length=50), nullable=False),
    sa.Column('identifier', sa.String(length=10), nullable=False),
    sa.Column('begin_shift_time', sa.DateTime(), nullable=False),
    sa.Column('end_shift_time', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('batch_number', 'batch_date', name='batch')
    )
    op.create_index(op.f('ix_shift_tasks_id'), 'shift_tasks', ['id'], unique=False)
    op.create_table('unique_codes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('unique_code', sa.String(length=30), nullable=False),
    sa.Column('shift_task', sa.Integer(), nullable=True),
    sa.Column('is_aggregated', sa.Boolean(), nullable=True),
    sa.Column('aggregated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['shift_task'], ['shift_tasks.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('unique_code', name='code')
    )
    op.create_index(op.f('ix_unique_codes_id'), 'unique_codes', ['id'], unique=False)
    op.create_index(op.f('ix_unique_codes_shift_task'), 'unique_codes', ['shift_task'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_unique_codes_shift_task'), table_name='unique_codes')
    op.drop_index(op.f('ix_unique_codes_id'), table_name='unique_codes')
    op.drop_table('unique_codes')
    op.drop_index(op.f('ix_shift_tasks_id'), table_name='shift_tasks')
    op.drop_table('shift_tasks')
    # ### end Alembic commands ###