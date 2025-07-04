from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

# Alembic Config 對象，提供對 .ini 文件中值的訪問
config = context.config

# 設置 Python 日誌
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 導入你的模型並設置 target_metadata
from models.base import Base
target_metadata = Base.metadata  # 指向你的模型的 MetaData

def run_migrations_offline() -> None:
    """以 'offline' 模式運行遷移"""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """以 'online' 模式運行遷移"""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()