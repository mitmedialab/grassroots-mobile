from sqlalchemy import *
from migrate import *

meta = MetaData()

customers = Table(
  'customers', meta,
   Column('id', Integer, primary_key = True),
   Column('msisdn', String(15)),
   Column('created', TIMESTAMP),
   Column('action', String(255)),
   Column('status', String(255))
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    customers.create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    customers.drop()
    pass
