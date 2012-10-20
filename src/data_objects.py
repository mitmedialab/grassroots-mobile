from sqlalchemy import *
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
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

class Customer(Base):
  __tablename__ = 'customers'
  id = Column(Integer, primary_key = True)
  msisdn = Column(String(15))
  created = Column(TIMESTAMP)
  action = Column(String(255))
  status = Column(String(255))
  outgoing_messages = relationship("OutgoingMessage",
                        order_by="desc(created)",
                        primaryjoin = "OutgoingMessage.customer_id==Customer.id")

class MessageTemplate(Base):
  __tablename__ = 'message_template'
  id = Column(Integer, primary_key = True)
  created = Column(TIMESTAMP)
  text = Column(String(140))
  outgoing_messages = relationship("OutgoingMessage",
                        order_by="desc(created)",
                        primaryjoin = "OutgoingMessage.message_template_id==MessageTemplate.id")

class OutgoingMessage(Base):
  __tablename__ = 'outgoing_messages'
  id = Column(Integer, primary_key = True)
  created = Column(TIMESTAMP)
  customer_id = Column(Integer, ForeignKey('customers.id'))
  customer = relationship(Customer, primaryjoin="OutgoingMessage.customer_id == Customer.id")
  handled = Column(Boolean, default = False)
  message_template_id = Column(Integer) #TODO: set up relationships
  message_template = relationship(MessageTemplate, 
                       primaryjoin="OutgoingMessage.message_template_id == MessageTemplate.id")

class Consumption(Base):
  __tablename__ = 'consumption'
  id = Column(Integer, primary_key = True)
  created = Column(TIMESTAMP)
  total_consumed = Column(Float)
  consumed_since_last_report = Column(Float)
  session = Column(Integer)

class ShutoffCommand(Base):
  __tablename__ = 'shutoff_commands'
  id = Column(Integer, primary_key = True)
  created = Column(TIMESTAMP)
  handled = Column(Boolean, default = False)

class IncomingMessage(Base):
  __tablename__ = 'incoming_messages'
  id = Column(Integer, primary_key = True)
  created = Column(TIMESTAMP)
  customer_id = Column(Integer)
  customer = relationship(Customer,
                          primaryjoin="IncomingMessage.customer_id == Customer.id")
  message = Column(String(255))
  handled = Column(Boolean, default = False)


  

#session.query(MeterState).all()
