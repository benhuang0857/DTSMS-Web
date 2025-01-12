"""create actions table

Revision ID: 15371e328044
Revises: c2243997988d
Create Date: 2024-12-28 19:11:03.063142

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision: str = '15371e328044'
down_revision: Union[str, None] = 'c2243997988d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'actions',
        sa.Column('id', sa.BigInteger, primary_key=True, index=True),
        sa.Column('automation_id', sa.Integer, sa.ForeignKey('automations.id', ondelete='SET NULL'), nullable=True),
        sa.Column('api_type', sa.String(255), nullable=True),
        sa.Column('endpoint', sa.String(255), nullable=True),
        sa.Column('command', sa.JSON, nullable=True),
        sa.Column('note', sa.String(255), server_default="active"),
        sa.Column('status', sa.String(50), server_default="process"),
        sa.Column('created_time', sa.TIMESTAMP, server_default=func.now(), nullable=False),
        sa.Column('updated_time', sa.TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('actions')
