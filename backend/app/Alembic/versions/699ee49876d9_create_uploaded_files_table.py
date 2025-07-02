"""Create files table

Revision ID: 699ee49876d9
Revises: 9bd57524e5df
Create Date: 2025-06-21 19:00:49.170663

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '699ee49876d9'
down_revision: Union[str, Sequence[str], None] = '9bd57524e5df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

pg_enum_tracking_status = postgresql.ENUM('pending', 'in_progress', 'success', 'error', 'dangerous', name='tracking_status')

tracking_status_enum = sa.Enum(
    'pending', 'in_progress', 'success', 'error', 'dangerous',
    name='tracking_status'
).with_variant(
    postgresql.ENUM(
        'pending', 'in_progress', 'success', 'error', 'dangerous',
        name='tracking_status',
        create_type=False
    ),
    'postgresql'
)


def upgrade() -> None:
    """Upgrade schema."""
    pg_enum_tracking_status.create(op.get_bind(), checkfirst=True)

    op.create_table(
        'uploaded_files',
        sa.Column('id', sa.BigInteger, primary_key=True, comment="檔案上傳ID"),
        sa.Column('user_id', sa.BigInteger, sa.ForeignKey('users.id', ondelete='SET NULL'), nullable=False, comment="用戶ID"),
        sa.Column('ticket_num', sa.String(255), nullable=False, unique=True, comment="單號"),
        sa.Column('name', sa.String(255), nullable=False, comment="檔案名稱"),
        sa.Column('ftype', sa.String(50), nullable=False, comment="檔案類型"),
        sa.Column('fsize', sa.BigInteger, nullable=False, comment="檔案大小（位元組）"),
        sa.Column('unzip_password', sa.String(255), nullable=True, comment="解壓縮密碼"),
        sa.Column('description', sa.String(255), nullable=True, comment="檔案描述"),
        sa.Column('status', tracking_status_enum, server_default="pending", nullable=False, comment="處理狀態"),
        sa.Column('created_time', sa.TIMESTAMP, server_default=func.now(), nullable=False),
        sa.Column('updated_time', sa.TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False),
    )
    op.create_table(
        'tickets',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('ticket_num', sa.String(255), nullable=False, unique=True, comment="單號"),
        sa.Column(
            'status',
            sa.Enum(
                'active', 'inactive', 'banned', name='basic_status'
            ).with_variant(
                postgresql.ENUM('active', 'inactive', 'banned', name='basic_status', create_type=False),
                'postgresql'
            ),
            server_default="active",
            nullable=False,
            comment="狀態"
        ),
        sa.Column('created_time', sa.TIMESTAMP, server_default=func.now(), nullable=False),
        sa.Column('updated_time', sa.TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False),
    )
    op.create_table(
        'processing_steps',
        sa.Column('id', sa.BigInteger, primary_key=True, comment="處理步驟ID"),
        sa.Column('autoflow_id', sa.BigInteger, sa.ForeignKey('autoflows.id'), nullable=True, comment="關聯掃描自動化腳本ID"),
        sa.Column('name', sa.String(50), nullable=False, comment="步驟名稱"),
        sa.Column('description', sa.Text, nullable=True, comment="步驟描述"),
        sa.Column('created_time', sa.TIMESTAMP, server_default=func.now(), nullable=False),
        sa.Column('updated_time', sa.TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False),
    )
    op.create_table(
        'file_trackings',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('tracking_id', UUID(as_uuid=True), unique=True, nullable=False, server_default=sa.text("gen_random_uuid()"), comment="唯一追蹤ID"),
        sa.Column('uploaded_file_id', sa.BigInteger, sa.ForeignKey('uploaded_files.id'), nullable=False, comment="關聯檔案ID"),
        sa.Column('step_id', sa.BigInteger, sa.ForeignKey('processing_steps.id'), nullable=False, comment="關聯處理步驟ID"),
        sa.Column('start_time', sa.TIMESTAMP, nullable=False, comment="開始時間"),
        sa.Column('end_time', sa.TIMESTAMP, nullable=True, comment="結束時間"),
        sa.Column('result', sa.String(255), nullable=True, comment="處理結果"),
        sa.Column('status', tracking_status_enum, server_default="pending", nullable=False, comment="處理狀態"),
        sa.Column('note', sa.Text, nullable=True, comment="備註"),
        sa.Column('created_time', sa.TIMESTAMP, server_default=func.now(), nullable=False),
        sa.Column('updated_time', sa.TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('file_trackings')
    op.drop_table('tickets')
    op.drop_table('processing_steps')
    op.drop_table('uploaded_files')

    pg_enum_tracking_status.drop(op.get_bind(), checkfirst=True)
