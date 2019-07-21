import os
import time
import logging

from dotenv import load_dotenv
from sqlalchemy import create_engine, orm, MetaData
import phonenumbers

load_dotenv()

PG_HOST = os.environ.get('PG_HOST')
PG_PORT = os.environ.get('PG_PORT')
PG_DB = os.environ.get('PG_DB')
PG_TABLE = os.environ.get('PG_TABLE')
PG_USER = os.environ.get('PG_USER')
PG_PWD = os.environ.get('PG_PWD')
PG_NEW_COLUMN_NAME = os.environ.get('PG_NEW_COLUMN_NAME')

DELAY = 30

logging.basicConfig(
        format='%(asctime)s,%(msecs)d %(levelname)s: %(message)s',
        datefmt='%H:%M:%S',
        )

engine = create_engine(f'postgresql://{PG_USER}:{PG_PWD}@{PG_HOST}:{PG_PORT}/{PG_DB}')
conn = engine.connect()

class Order(object):
    pass

meta = MetaData(bind=engine, reflect=True)
orm.Mapper(Order, meta.tables[f'{PG_TABLE}'])

while True:
    try:
        session = orm.Session(bind=engine)
        orders = session.query(Order).filter(getattr(Order, PG_NEW_COLUMN_NAME) == '')
        mapping = []
        for order in orders:
            try:
                phonenumber = phonenumbers.parse(order.contact_phone, 'RU').national_number
                mapping.append({'id': order.id, f'{PG_NEW_COLUMN_NAME}': phonenumber})
            except Exception as e:
                logging.warning(f'{e} at order.id #{order.id}')
        session.bulk_update_mappings(Order, mapping)
        session.commit()
    except Exception as e:
        logging.warning('Connection or query error')
    time.sleep(DELAY)
