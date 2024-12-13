"""create user table

Revision ID: 63f4b6faef3d
Revises: 
Create Date: 2024-12-13 13:53:32.364818

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision: str = '63f4b6faef3d'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('username', sa.String, unique=True, index=True),
        sa.Column('email', sa.String, unique=True, index=True),
        sa.Column('avatar', sa.String, nullable=True),
        sa.Column('real_name', sa.String, nullable=True),
        sa.Column('organization', sa.String, nullable=True),
        sa.Column('address', sa.String, nullable=True),
        sa.Column('mobile', sa.String, nullable=True),
        sa.Column('password', sa.String),
        sa.Column('created_time', sa.TIMESTAMP, server_default=func.now(), nullable=False),
        sa.Column('updated_time', sa.TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('users')
