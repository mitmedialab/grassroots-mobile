from sqlalchemy import *
from migrate import *

meta = MetaData()

message_templates = Table(
  'message_templates', meta,
   Column('id', Integer, primary_key = True),
   Column('created', TIMESTAMP),
   Column('text', String(140))
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    message_templates.create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    message_templates.drop()
    pass
