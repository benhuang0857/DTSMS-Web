"""create logs table

Revision ID: 818af49a3fb8
Revises: b7933248257c
Create Date: 2024-12-28 13:57:56.955379

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision: str = '818af49a3fb8'
down_revision: Union[str, None] = 'b7933248257c'
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
