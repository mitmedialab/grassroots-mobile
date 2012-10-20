from sqlalchemy import *
from migrate import *

meta = MetaData()

consumption = Table(
  'consumption', meta,
   Column('id', Integer, primary_key = True),
   Column('created', TIMESTAMP),
   Column('total_consumed', Float),
   Column('consumed_since_last_report', Float),
   Column('session', Integer) #relates to shutoff commands?
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    consumption.create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    consumption.drop()
    pass
