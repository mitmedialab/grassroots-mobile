from sqlalchemy import *
from migrate import *

meta = MetaData()

meter_states = Table(
  'meter_states', meta,
  Column('id', Integer, primary_key = True),
  Column('created', TIMESTAMP),
  Column('balance', Float),
  Column('action', String(255))
)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    meter_states.create()
    pass

def downgrade(migrate_engine):
    meta.bind = migrate_engine
    meter_states.drop()
    pass
