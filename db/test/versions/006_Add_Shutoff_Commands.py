from sqlalchemy import *
from migrate import *

meta = MetaData()

shutoff_commands = Table(
  'shutoff_commands', meta,
   Column('id', Integer, primary_key = True),
   Column('created', TIMESTAMP),
   Column('command', String(4)),
   Column('handled', Boolean, default = False)
)


def upgrade(migrate_engine):
    meta.bind = migrate_engine
    shutoff_commands.create()
    pass


def downgrade(migrate_engine):
    meta.bind = migrate_engine
    shutoff_commands.drop()
    pass
