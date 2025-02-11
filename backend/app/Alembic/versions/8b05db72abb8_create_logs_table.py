"""Create logs table

Revision ID: 8b05db72abb8
Revises: 1f6bf597b47e
Create Date: 2025-02-11 11:35:29.885540

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision: str = '8b05db72abb8'
down_revision: Union[str, None] = '1f6bf597b47e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'logs',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('level', sa.String(50), nullable=False),
        sa.Column('message', sa.Text, nullable=False),  # Changed to Text for potentially large log messages
        sa.Column('created_time', sa.TIMESTAMP, server_default=func.now(), nullable=False),
        sa.Column('updated_time', sa.TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('logs')
