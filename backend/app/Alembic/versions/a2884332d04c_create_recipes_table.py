"""Create recipes table

Revision ID: a2884332d04c
Revises: 35293c414236
Create Date: 2025-06-21 18:50:17.063094

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'a2884332d04c'
down_revision: Union[str, Sequence[str], None] = '35293c414236'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'recipes',
        sa.Column('id', sa.BigInteger, primary_key=True, comment="站點自動化腳本ID"),
        sa.Column('library_id', sa.Integer, sa.ForeignKey('libraries.id', ondelete='SET NULL'), nullable=True, comment="Library ID"),
        sa.Column('name', sa.String(255), nullable=False, comment="腳本名稱"),
        sa.Column('description', sa.Text, nullable=True, comment="腳本描述"),
        sa.Column(
            'status',
            sa.Enum(
                'active', 'inactive', 'banned', name='basic_status'
            ).with_variant(
                postgresql.ENUM('active', 'inactive', 'banned', name='basic_status', create_type=False),
                'postgresql'
            ),
            server_default="active",
            nullable=False,
            comment="狀態"
        ),
        sa.Column('allow_parallel_autoflows', sa.Boolean, nullable=False, server_default="false", comment="是否允許Autoflow並行執行"),
        sa.Column('created_time', sa.TIMESTAMP, server_default=func.now(), nullable=False),
        sa.Column('updated_time', sa.TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False),
    )
    op.create_table(
        'recipe_steps',
        sa.Column('id', sa.BigInteger, primary_key=True, comment="站點腳本步驟ID"),
        sa.Column('recipe_id', sa.BigInteger, sa.ForeignKey('recipes.id', ondelete='CASCADE'), nullable=False, comment="腳本ID"),
        sa.Column('number', sa.Integer, nullable=False, comment="步驟序號"),
        sa.Column('action', sa.String(50), nullable=False, comment="執行動作"),
        sa.Column('parameters', sa.JSON, nullable=True, comment="參數"),
        sa.Column(
            'status',
            sa.Enum(
                'active', 'inactive', 'banned', name='basic_status'
            ).with_variant(
                postgresql.ENUM('active', 'inactive', 'banned', name='basic_status', create_type=False),
                'postgresql'
            ),
            server_default="active",
            nullable=False,
            comment="狀態"
        ),
        sa.Column('created_time', sa.TIMESTAMP, server_default=func.now(), nullable=False),
        sa.Column('updated_time', sa.TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('recipe_steps')
    op.drop_table('recipes')
