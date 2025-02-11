"""Create reports table

Revision ID: 27b639797116
Revises: fc2fd64785a0
Create Date: 2025-02-11 11:38:43.427413

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision: str = '27b639797116'
down_revision: Union[str, None] = 'fc2fd64785a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'reports',
        sa.Column('id', sa.BigInteger, primary_key=True, index=True),
        sa.Column('file_upload_id', sa.BigInteger, sa.ForeignKey('file_uploads.id', ondelete='CASCADE')),
        sa.Column('user_id', sa.BigInteger, sa.ForeignKey('users.id', ondelete='SET NULL')),
        sa.Column('result', sa.JSON, nullable=True),
        sa.Column('token', sa.String(255), nullable=True),
        sa.Column('status', sa.String(50), server_default="process"),
        sa.Column('created_time', sa.TIMESTAMP, server_default=func.now(), nullable=False),
        sa.Column('updated_time', sa.TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('reports')
