from sqlalchemy import *
from migrate import *

meta = MetaData()

incoming_messages = Table(
  'incoming_messages', meta,
   Column('id', Integer, primary_key = True),
   Column('created', TIMESTAMP),
   Column('customer_id', Integer),
   Column('message', String(255)),
   Column('handled', Boolean, default = False)
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    incoming_messages.create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    incoming_messages.drop()
    pass
