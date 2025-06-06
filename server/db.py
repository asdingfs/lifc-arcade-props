import sqlite3
from datetime import datetime

import click
from flask import current_app, g
from config.db_connection_pool import DbConnectionPool


def init_db():
  """Initialize the database."""
  db = open_db()

  with current_app.open_resource('schema.sql') as f:
    db.executescript(f.read().decode('utf8'))


@click.command('init-db')
def init_db_command():
  """Clear the existing data and create new tables."""
  init_db()
  click.echo('Initialized the database.')


def init_app(app):
  ensure_pool()
  app.teardown_appcontext(close_pool)
  app.cli.add_command(init_db_command)


def ensure_pool():
  if 'db' not in g:
    g.db = DbConnectionPool(current_app.config['DATABASE'], 5)


def open_db():
  return g.db.get()


def close_db(db_conn):
  """Close the database connection."""
  return None if ('db' not in g or db_conn is None) else g.db.forgo(db_conn)


def close_pool(db_conn):
  """'Close the database connection, essentially returning it to the pool."""
  """Close the database connection."""
  db = g.pop('db', None)
  if db is not None:
    db.close_all()


sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)
