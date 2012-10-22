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

# balance refers to the total balance for that session
# rather than the balance remaining.
# Balance Remaining is calculated by combining meter state and consumption
# == meter states ==
# topup: credit added
# shutdown: no credit; meter shut down
# started: no credit; meter shut down
class MeterState(Base):
  __tablename__ = 'meter_states'
  id = Column(Integer, primary_key = True)
  created = Column(TIMESTAMP, default=func.now())
  balance = Column(Float)
  action = Column(String(255))

  @staticmethod
  def latest():
    state = session.query(MeterState).all()
    if(len(state) > 0): return state[-1]
    return None


# customer statuses:
# new: customer created, first message not processed
# topup_offered_inactive:   topup offered, but not confirmed, inactive customer
# topup_offered_active: topup offered, but not confirmed, active customer
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
  total_consumed = Column(Float) #kilowatt-minutes
  consumed_since_last_report = Column(Float)
  session = Column(Integer) #TODO: session doesn't exist yet
  kilowatt_minutes_per_credit = 1.0

  @staticmethod
  def latest():
    state = session.query(Consumption).all()
    if(len(state) > 0): return state[-1]
    return None

  def credits_to_kilowatt_minutes(self,credits):
    return float(credits) * self.kilowatt_minutes_per_credit

  def credits_used(self):
    return self.total_consumed / self.kilowatt_minutes_per_credit


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

  def set_handled(self):
    self.handled = True
    session.add(self)
    session.commit()
  
# session = Session()
# session.query(MeterState).all()
