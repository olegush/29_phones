import os
import time
import logging

from dotenv import load_dotenv
from sqlalchemy import create_engine, orm, MetaData, exc, Column, String, Integer
import phonenumbers

load_dotenv()

PG_URL = os.environ.get('PG_URL')
PG_TABLE = os.environ.get('PG_TABLE')

DELAY = 60 * 3

logging.basicConfig(
        format='%(asctime)s,%(msecs)d %(levelname)s: %(message)s',
        datefmt='%H:%M:%S',
        )

engine = create_engine(PG_URL)
conn = engine.connect()

class Order(object):
    __table__ = PG_TABLE
    id = Column(Integer)
    contact_phone = Column(String(100))
    contact_phone_normalized = Column(String(100))

meta = MetaData(bind=engine, reflect=True)
orm.Mapper(Order, meta.tables[PG_TABLE])

while True:
    try:
        session = orm.Session(bind=engine)
        orders = session.query(Order).filter(Order.contact_phone_normalized == '')
        mapping = []
        for order in orders:
            try:
                phonenumber = phonenumbers.parse(order.contact_phone, 'RU').national_number
                mapping.append({'id': order.id, 'contact_phone_normalized': phonenumber})
            except Exception as e:
                logging.warning(f'{e} at order.id #{order.id}')
        session.bulk_update_mappings(Order, mapping)
        session.commit()
    except exc.OperationalError:
        logging.warning('Connection error occured')
    except Exception as e:
        logging.critical(e)
    time.sleep(DELAY)
