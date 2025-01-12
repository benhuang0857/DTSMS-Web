"""create file_uploads table

Revision ID: 87d9ff00c124
Revises: 63f4b6faef3d
Create Date: 2024-12-13 16:07:58.994789

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision: str = '87d9ff00c124'
down_revision: Union[str, None] = '63f4b6faef3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'file_uploads',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('tracking_num', sa.String, unique=True, index=True),
        sa.Column('user', sa.String, unique=True),
        sa.Column('token', sa.String, nullable=True),
        sa.Column('status', sa.String, default='process'),
        sa.Column('created_time', sa.TIMESTAMP, server_default=func.now(), nullable=False),
        sa.Column('updated_time', sa.TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False),
    )

def downgrade() -> None:
    op.drop_table('file_uploads')
