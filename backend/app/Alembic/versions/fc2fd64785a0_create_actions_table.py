"""Create actions table

Revision ID: fc2fd64785a0
Revises: 2ae31b82cbe5
Create Date: 2025-02-11 11:38:02.764927

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision: str = 'fc2fd64785a0'
down_revision: Union[str, None] = '2ae31b82cbe5'
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
