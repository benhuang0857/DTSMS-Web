"""create automations table

Revision ID: 9eaa05cc449b
Revises: 15371e328044
Create Date: 2024-12-28 19:17:41.729443

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision: str = '9eaa05cc449b'
down_revision: Union[str, None] = 'c2243997988d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'automations',
        sa.Column('id', sa.BigInteger, primary_key=True, index=True),
        sa.Column('user_id', sa.BigInteger, sa.ForeignKey('users.id', ondelete='SET NULL')),
        sa.Column('note', sa.String(255), server_default="active"),
        sa.Column('status', sa.String(50), server_default="process"),
        sa.Column('created_time', sa.TIMESTAMP, server_default=func.now(), nullable=False),
        sa.Column('updated_time', sa.TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('automations')
