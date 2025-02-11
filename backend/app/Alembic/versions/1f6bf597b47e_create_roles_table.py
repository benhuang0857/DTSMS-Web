"""Create roles table

Revision ID: 1f6bf597b47e
Revises: 8b16e89b7c96
Create Date: 2025-02-11 11:34:48.979009

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision: str = '1f6bf597b47e'
down_revision: Union[str, None] = '8b16e89b7c96'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
        op.create_table(
        'roles',
        sa.Column('id', sa.BigInteger, primary_key=True, index=True),
        sa.Column('title', sa.String, unique=True),
        sa.Column('status', sa.String(50), server_default="active"),
        sa.Column('note', sa.String(255), server_default="active"),
        sa.Column('created_time', sa.TIMESTAMP, server_default=func.now(), nullable=False),
        sa.Column('updated_time', sa.TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('roles')
