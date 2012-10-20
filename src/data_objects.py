from sqlalchemy import *
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

db = create_engine('sqlite:///db/sqlite/test.db', echo=True)
Session = sessionmaker(bind=db)
Base = declarative_base()

class MeterState(Base):
  __tablename__ = 'meter_states'
  id = Column(Integer, primary_key = True)
  created = Column(TIMESTAMP)
  balance = Column(Float)
  action = Column(String(255))

#session.query(MeterState).all()
