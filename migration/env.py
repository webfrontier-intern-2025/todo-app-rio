import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
print(f"✅ sys.path に追加済み: {os.path.join(os.path.dirname(__file__), '..', 'src')}")

from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from app.database import Base
from models.todo import Todo
from models.tag import Tag

# =========================================
# ✅ 「src」ディレクトリをPythonパスに追加
# =========================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)
print(f"✅ sys.path に追加済み: {SRC_DIR}")

# =========================================
# ✅ モジュールのインポート
# =========================================
from app.database import Base  # noqa: E402
from app.settings import DATABASE_URL  # noqa: E402
from models.todo import Todo  # noqa: E402, F401

# =========================================
# ✅ Alembic 設定
# =========================================
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata
config.set_main_option("sqlalchemy.url", DATABASE_URL)


# =========================================
# ✅ マイグレーション関数
# =========================================
def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection,
                          target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
