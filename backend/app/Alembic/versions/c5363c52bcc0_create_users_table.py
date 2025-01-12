"""create users table

Revision ID: c5363c52bcc0
Revises: 
Create Date: 2024-12-28 13:53:36.727381

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision: str = 'c5363c52bcc0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('username', sa.String(50), unique=True, index=True),
        sa.Column('email', sa.String(255), unique=True, index=True),
        sa.Column('avatar', sa.String(255), nullable=True),
        sa.Column('real_name', sa.String(100), nullable=True),
        sa.Column('organization', sa.String(100), nullable=True),
        sa.Column('address', sa.String(255), nullable=True),
        sa.Column('mobile', sa.String(15), nullable=True),
        sa.Column('password', sa.String(255), nullable=False),  # Password should not be nullable
        sa.Column('status', sa.String(50), server_default="active", nullable=False),
        sa.Column('created_time', sa.TIMESTAMP, server_default=func.now(), nullable=False),
        sa.Column('updated_time', sa.TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('users')
