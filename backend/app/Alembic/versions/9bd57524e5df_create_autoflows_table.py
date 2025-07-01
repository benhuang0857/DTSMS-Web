"""Create autoflows table

Revision ID: 9bd57524e5df
Revises: a2884332d04c
Create Date: 2025-06-21 18:53:05.990772

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '9bd57524e5df'
down_revision: Union[str, Sequence[str], None] = 'a2884332d04c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'autoflows',
        sa.Column('id', sa.BigInteger, primary_key=True, comment="掃描自動化流程ID"),
        sa.Column('recipe_id', sa.BigInteger, sa.ForeignKey('recipes.id', ondelete='SET NULL'), nullable=True, comment="腳本ID"),
        sa.Column('name', sa.String(255), nullable=False, comment="流程名稱"),
        sa.Column('description', sa.Text, nullable=True, comment="流程描述"),
        sa.Column(
            'status',
            sa.Enum('active', 'inactive', 'banned', name='autoflow_status'),
            server_default="active",
            nullable=False,
            comment="狀態"
        ),
        sa.Column('created_time', sa.TIMESTAMP, server_default=func.now(), nullable=False),
        sa.Column('updated_time', sa.TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('autoflows')
    
    user_status = postgresql.ENUM('active', 'inactive', 'banned', name='autoflow_status')
    user_status.drop(op.get_bind(), checkfirst=True)
