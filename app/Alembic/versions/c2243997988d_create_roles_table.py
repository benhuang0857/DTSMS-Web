"""create roles table

Revision ID: c2243997988d
Revises: 82bdd37d174f
Create Date: 2024-12-28 14:37:08.572036

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func


# revision identifiers, used by Alembic.
revision: str = 'c2243997988d'
down_revision: Union[str, None] = '82bdd37d174f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'roles',
        sa.Column('id', sa.BigInteger, primary_key=True, index=True),
        sa.Column('title', sa.String, unique=True),
        sa.Column('status', sa.String(50), server_default="active"),
        sa.Column('note', sa.String(255), server_default="active"),
        sa.Column('created_time', sa.TIMESTAMP, server_default=func.now(), nullable=False),
        sa.Column('updated_time', sa.TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('roles')
