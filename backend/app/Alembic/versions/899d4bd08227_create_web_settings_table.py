"""Create web_settings table

Revision ID: 899d4bd08227
Revises: 699ee49876d9
Create Date: 2025-06-21 19:54:25.500280

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '899d4bd08227'
down_revision: Union[str, Sequence[str], None] = '699ee49876d9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'web_settings',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('key', sa.String(length=255), nullable=False, unique=True),
        sa.Column('name', sa.String(length=255), nullable=False, comment="設定名稱"),
        sa.Column('description', sa.String(length=255), nullable=True, comment="設定描述"),
        sa.Column('value', sa.Text(), nullable=False),
        sa.Column(
            'status',
            sa.Enum('on', 'off', name='web_setting_status'),
            server_default="on",
            nullable=False,
            comment="狀態"
        ),
        sa.Column('created_time', sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_time', sa.DateTime(), server_default=sa.func.now(), onupdate=sa.func.now(), nullable=False),
    )

    # 插入預設設定值
    conn = op.get_bind()
    conn.execute(
        sa.text(
            """
            INSERT INTO web_settings (key, name, value, status, created_time, updated_time)
            VALUES 
            (:key1, :name1, :value1, 'on', NOW(), NOW()),
            (:key2, :name2, :value2, 'on', NOW(), NOW())
            """
        ),
        {
            "key1": "file_size_limit",
            "name1": "檔案大小限制",
            "value1": "500MB",
            "key2": "file_extension",
            "name2": "檔案種類",
            "value2": "exe,zip,tar,jpg,png",
        }
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('web_settings')

    user_status = postgresql.ENUM('on', 'off', name='web_setting_status')
    user_status.drop(op.get_bind(), checkfirst=True)
