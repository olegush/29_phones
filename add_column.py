import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, orm, MetaData, Table, Column, String
from alembic.migration import MigrationContext
from alembic.operations import Operations

load_dotenv()

PG_HOST = os.environ.get('PG_HOST')
PG_PORT = os.environ.get('PG_PORT')
PG_DB = os.environ.get('PG_DB')
PG_TABLE = os.environ.get('PG_TABLE')
PG_USER = os.environ.get('PG_USER')
PG_PWD = os.environ.get('PG_PWD')
PG_NEW_COLUMN_NAME = os.environ.get('PG_NEW_COLUMN_NAME')

engine = create_engine(f'postgresql://{PG_USER}:{PG_PWD}@{PG_HOST}:{PG_PORT}/{PG_DB}')

context = MigrationContext.configure(engine.connect())
operation = Operations(context)
operation.add_column(f'{PG_TABLE}', Column(f'{PG_NEW_COLUMN_NAME}', String(100)))

metadata = MetaData()
metadata.reflect(bind=engine)
keys = metadata.tables[f'{PG_TABLE}'].columns.keys()
print(f'All columns of the table "{PG_TABLE}": {keys}')
