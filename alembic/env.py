from __future__ import with_statement
import os
import sys
from alembic import context
from sqlalchemy import engine_from_config, pool
from logging.config import fileConfig
from alembic.config import Config

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = Config("alembic.ini")

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
cwd = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(cwd)
settings = os.path.join(cwd, 'etc/settings.py')
if not os.path.exists(settings):
    settings = os.path.join(cwd, 'etc/dev_config.py')

if 'JUNE_SETTINGS' not in os.environ:
    os.environ['JUNE_SETTINGS'] = settings

from june.app import create_app
from june.models import db
app = create_app()
# set the database url
config.set_main_option(
    'sqlalchemy.url',
    app.config.get('SQLALCHEMY_DATABASE_URI')
)
target_metadata = db.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url)

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    engine = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool
    )

    connection = engine.connect()
    context.configure(
        connection=connection,
        target_metadata=target_metadata
    )

    try:
        with context.begin_transaction():
            context.run_migrations()
    finally:
        connection.close()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()