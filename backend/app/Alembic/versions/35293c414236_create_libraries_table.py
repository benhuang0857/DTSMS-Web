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
        sa.Column('api_endpoint', sa.String(500), nullable=False, comment="API Endpoint URL"),
        sa.Column('docker_image', sa.String(255), nullable=True, comment="Docker Image Name (Optional for custom deployments)"),
        sa.Column('docker_tag', sa.String(100), nullable=True, default='latest', comment="Docker Image Tag"),
        sa.Column('api_key', sa.String(255), nullable=True, comment="API Authentication Key"),
        sa.Column('api_headers', sa.JSON, nullable=True, comment="Additional API Headers"),
        sa.Column('timeout_seconds', sa.Integer, nullable=True, default=30, comment="API Request Timeout"),
        sa.Column('retry_count', sa.Integer, nullable=True, default=3, comment="API Request Retry Count"),
        sa.Column('docker_env_vars', sa.JSON, nullable=True, comment="Docker Environment Variables"),
        sa.Column('docker_ports', sa.JSON, nullable=True, comment="Docker Port Mappings"),
        sa.Column('docker_volumes', sa.JSON, nullable=True, comment="Docker Volume Mappings"),
        sa.Column('health_check_endpoint', sa.String(500), nullable=True, comment="Health Check API Endpoint"),
        sa.Column('description', sa.String(500), nullable=True, comment="Library Description"),
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
        sa.Column('created_time', sa.TIMESTAMP, server_default=func.now(), nullable=False, comment="Creation Time"),
        sa.Column('updated_time', sa.TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False, comment="Update Time"),
    )
    op.create_table(
        'library_actions',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('library_id', sa.BigInteger, sa.ForeignKey('libraries.id', ondelete='CASCADE'), nullable=False, comment="Library ID"),
        sa.Column('name', sa.String(100), nullable=False, comment="Action Name (e.g., '一般掃描', '進階掃描')"),
        sa.Column('api_path', sa.String(200), nullable=False, comment="API Path (e.g., '/scan/basic', '/scan/advanced')"),
        sa.Column('http_method', sa.String(10), nullable=False, server_default='POST', comment="HTTP Method (GET, POST, PUT, DELETE)"),
        sa.Column('request_schema', sa.JSON, nullable=True, comment="Request body schema/parameters"),
        sa.Column('response_schema', sa.JSON, nullable=True, comment="Expected response schema"),
        sa.Column('description', sa.String(500), nullable=True, comment="Action Description"),
        sa.Column('execution_order', sa.Integer, nullable=True, comment="Suggested execution order in workflows"),
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
        sa.Column('created_time', sa.TIMESTAMP, server_default=func.now(), nullable=False, comment="Creation Time"),
        sa.Column('updated_time', sa.TIMESTAMP, server_default=func.now(), onupdate=func.now(), nullable=False, comment="Update Time"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('library_actions')
    op.drop_table('libraries')
