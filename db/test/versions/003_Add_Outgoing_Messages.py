from sqlalchemy import *
from migrate import *

meta = MetaData()

outgoing_messages = Table(
  'outgoing_messages', meta,
   Column('id', Integer, primary_key = True),
   Column('created', TIMESTAMP),
   Column('customer_id', Integer),
   Column('message_template_id', Integer),
   Column('handled', Boolean, default = False)
)

def upgrade(migrate_engine):
    meta.bind = migrate_engine
    outgoing_messages.create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    outgoing_messages.drop()
    pass
