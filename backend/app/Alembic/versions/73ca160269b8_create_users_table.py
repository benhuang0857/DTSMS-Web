"""Create users table

Revision ID: 73ca160269b8
Revises: 
Create Date: 2025-06-21 16:35:39.743646
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
from passlib.context import CryptContext

# revision identifiers, used by Alembic.
revision: str = '73ca160269b8'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 建立 Postgres 專用 ENUM 物件
pg_enum_basic_status = postgresql.ENUM('active', 'inactive', 'banned', name='basic_status')

def upgrade() -> None:
    """Upgrade schema."""

    # 建立 ENUM type，如果還沒存在的話
    pg_enum_basic_status.create(op.get_bind(), checkfirst=True)

    # 創建 roles 表
    op.create_table(
        'roles',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('name', sa.String(50), unique=True, index=True, comment="角色名稱"),
        sa.Column('description', sa.String(255), nullable=True, comment="角色描述"),
        sa.Column('created_time', sa.TIMESTAMP, server_default=func.now(), nullable=False, comment="創建時間"),
        sa.Column('updated_time', sa.TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新時間"),
    )

    # 插入預設角色
    conn = op.get_bind()
    conn.execute(
        sa.text(
            "INSERT INTO roles (name, description, created_time, updated_time) VALUES "
            "(:name, :description, NOW(), NOW())"
        ),
        {"name": "admin", "description": "系統管理員"}
    )
    conn.execute(
        sa.text(
            "INSERT INTO roles (name, description, created_time, updated_time) VALUES "
            "(:name, :description, NOW(), NOW())"
        ),
        {"name": "member", "description": "普通用戶"}
    )

    # 創建 users 表
    op.create_table(
        'users',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column(
            'role_id',
            sa.BigInteger,
            sa.ForeignKey('roles.id', ondelete='SET NULL', name='fk_users_role_id'),
            nullable=False,
            server_default='2',
            comment="角色ID"
        ),
        sa.Column('account', sa.String(50), unique=True, index=True, comment="帳戶"),
        sa.Column('email', sa.String(100), unique=True, index=True, comment="E-mail"),
        sa.Column('avatar', sa.String(255), nullable=True, comment="頭像"),
        sa.Column('real_name', sa.String(100), nullable=True, comment="真實姓名"),
        sa.Column('organization', sa.String(100), nullable=True, comment="組織"),
        sa.Column('address', sa.String(255), nullable=True, comment="地址"),
        sa.Column('mobile', sa.String(15), nullable=True, comment="手機號"),
        sa.Column('password', sa.String(255), nullable=False, comment="密碼"),
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
        sa.Column('created_time', sa.TIMESTAMP, server_default=func.now(), nullable=False, comment="創建時間"),
        sa.Column('updated_time', sa.TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False, comment="更新時間"),
    )

    # 插入預設管理員用戶
    hashed_password = pwd_context.hash("12345678")
    conn.execute(
        sa.text(
            """
            INSERT INTO users 
            (role_id, account, email, password, status, created_time, updated_time)
            VALUES 
            (
                (SELECT id FROM roles WHERE name = 'admin'), 
                :account, 
                :email, 
                :password, 
                'active', 
                NOW(), 
                NOW()
            )
            """
        ),
        {
            "account": "admin",
            "email": "admin@example.com",
            "password": hashed_password
        }
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_table('users')
    op.drop_table('roles')

    pg_enum_basic_status.drop(op.get_bind(), checkfirst=True)
