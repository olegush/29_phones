import os

from dotenv import load_dotenv
from sqlalchemy import create_engine, orm, MetaData, Table, Column, String
from alembic.migration import MigrationContext
from alembic.operations import Operations

load_dotenv()

PG_URL = os.environ.get('PG_URL')
PG_TABLE = os.environ.get('PG_TABLE')

engine = create_engine(PG_URL)
context = MigrationContext.configure(engine.connect())
operation = Operations(context)
operation.add_column(PG_TABLE, Column('contact_phone_normalized', String(100)))

metadata = MetaData()
metadata.reflect(bind=engine)
keys = metadata.tables[PG_TABLE].columns.keys()

print(f'All columns of the table "{PG_TABLE}": {keys}')
