"""Create file_uploads table

Revision ID: 9be0cbce97e6
Revises: 8b05db72abb8
Create Date: 2025-02-11 11:36:38.605069

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func

# revision identifiers, used by Alembic.
revision: str = '9be0cbce97e6'
down_revision: Union[str, None] = '8b05db72abb8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
        op.create_table(
        'file_uploads',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('tracking_num', sa.String(100), unique=True, index=True),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=True),
        sa.Column('token', sa.String(255), nullable=True),
        sa.Column('status', sa.String(50), server_default='process', nullable=False),
        sa.Column('created_time', sa.TIMESTAMP, server_default=func.now(), nullable=False),
        sa.Column('updated_time', sa.TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('file_uploads')
