"""Create libraries table

Revision ID: 35293c414236
Revises: 73ca160269b8
Create Date: 2025-06-21 18:42:35.803198

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '35293c414236'
down_revision: Union[str, Sequence[str], None] = '73ca160269b8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'libraries',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False, unique=True, comment="Library Name"),
        sa.Column('protocal', sa.String(50), nullable=True, comment="Protocol Type"),
        sa.Column('baudrate', sa.Integer, nullable=True, comment="Baudrate"),
        sa.Column('parity', sa.String(10), nullable=True, comment="Parity Type"),
        sa.Column('stopbits', sa.Integer, nullable=True, comment="Stop Bits"),
        sa.Column('bytesize', sa.Integer, nullable=True, comment="Byte Size"),
        sa.Column('host', sa.String(100), nullable=True, comment="Host Address"),
        sa.Column('port', sa.Integer, nullable=True, comment="Port Number"),
        sa.Column('certfile', sa.String(255), nullable=True, comment="Certificate File Path"),
        sa.Column('description', sa.String(255), nullable=True, comment="Library Description"),
        sa.Column(
            'status',
            sa.Enum('active', 'inactive', 'banned', name='library_status'),
            server_default="active",
            nullable=False,
            comment="狀態"
        ),
        sa.Column('created_time', sa.TIMESTAMP, server_default=func.now(), nullable=False, comment="Creation Time"),
        sa.Column('updated_time', sa.TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False, comment="Update Time"),
    )
    op.create_table(
        'actions',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('library_id', sa.BigInteger, sa.ForeignKey('libraries.id', ondelete='CASCADE'), nullable=False, comment="Library ID"),
        sa.Column('name', sa.String(100), nullable=False, comment="Action Name"),
        sa.Column('command', sa.String(255), nullable=False, comment="Command to Execute"),
        sa.Column('description', sa.String(255), nullable=True, comment="Action Description"),
        sa.Column(
            'status',
            sa.Enum('active', 'inactive', 'banned', name='library_status'),
            server_default="active",
            nullable=False,
            comment="狀態"
        ),
        sa.Column('created_time', sa.TIMESTAMP, server_default=func.now(), nullable=False, comment="Creation Time"),
        sa.Column('updated_time', sa.TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False, comment="Update Time"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('actions')
    op.drop_table('libraries')
        
    user_status = postgresql.ENUM('active', 'inactive', 'banned', name='library_status')
    user_status.drop(op.get_bind(), checkfirst=True)
