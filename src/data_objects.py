from sqlalchemy import *
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import scoped_session, sessionmaker

db = create_engine('sqlite:///db/sqlite/test.db', echo=False)
Session = sessionmaker(bind=db)
Base = declarative_base()

try:
  session
except NameError:
  session = Session()

class MeterState(Base):
  __tablename__ = 'meter_states'
  id = Column(Integer, primary_key = True)
  created = Column(TIMESTAMP, default=func.now())
  balance = Column(Float)
  action = Column(String(255))


# customer statuses:
# new: customer created, first message not processed
# topup_offered:   topup offered, but not confirmed
# active: topup confirmed and accepted
# inactive: not part of the current batch of people to be notified

class Customer(Base):
  __tablename__ = 'customers'
  id = Column(Integer, primary_key = True)
  msisdn = Column(String(15))
  created = Column(TIMESTAMP, default=func.now())
  action = Column(String(255))
  status = Column(String(255), default="new")
  status_value = Column(String(255))
  outgoing_messages = relationship("OutgoingMessage",
                        order_by="desc(OutgoingMessage.created)",
                        primaryjoin = "OutgoingMessage.customer_id==Customer.id")
  incoming_messages = relationship("IncomingMessage",
                        order_by="desc(IncomingMessage.created)",
                        primaryjoin = "IncomingMessage.customer_id==Customer.id")

class MessageTemplate(Base):
  __tablename__ = 'message_templates'
  id = Column(Integer, primary_key = True)
  created = Column(TIMESTAMP, default=func.now())
  text = Column(String(140))
  outgoing_messages = relationship("OutgoingMessage",
                        order_by="desc(MessageTemplate.created)",
                        primaryjoin = "OutgoingMessage.message_template_id==MessageTemplate.id")

class OutgoingMessage(Base):
  __tablename__ = 'outgoing_messages'
  id = Column(Integer, primary_key = True)
  created = Column(TIMESTAMP, default=func.now())
  customer_id = Column(Integer, ForeignKey('customers.id'))
  message = Column(String(255))
  customer = relationship(Customer, primaryjoin="OutgoingMessage.customer_id == Customer.id")
  handled = Column(Boolean, default = False)
  message_template_id = Column(Integer, ForeignKey('message_templates.id')) #TODO: set up relationships
  message_template = relationship(MessageTemplate, 
                       primaryjoin="OutgoingMessage.message_template_id == MessageTemplate.id")

class Consumption(Base):
  __tablename__ = 'consumption'
  id = Column(Integer, primary_key = True)
  created = Column(TIMESTAMP, default=func.now())
  total_consumed = Column(Float)
  consumed_since_last_report = Column(Float)
  session_id = Column(Integer) #TODO: session doesn't exist yet

class SwitchCommand(Base):
  __tablename__ = 'shutoff_commands'
  id = Column(Integer, primary_key = True)
  created = Column(TIMESTAMP, default=func.now())
  command = Column(String(4))
  handled = Column(Boolean, default = False)

class IncomingMessage(Base):
  __tablename__ = 'incoming_messages'
  id = Column(Integer, primary_key = True)
  created = Column(TIMESTAMP, default=func.now())
  customer_id = Column(Integer, ForeignKey("customers.id"))
  customer = relationship(Customer,
                          primaryjoin="IncomingMessage.customer_id == Customer.id")
  message = Column(String(255))
  handled = Column(Boolean, default = False)


  
# session = Session()
# session.query(MeterState).all()
