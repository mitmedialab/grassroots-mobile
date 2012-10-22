from data_objects import *
import re

class MessagePipelineController:

  def check_messages(self):
    return None

  #pipeline items which return "continue" pass through
  #pipeline items which return "halt" halt the queue
  #TODO: mark message as handled
  def process_message(self, message):

    status = self.confirm_topup_request(message)
    if status == "halt": return None

    status = self.topup_request(message)
    if status == "halt": return None
 
    status = self.process_balance_request(message)
    if status == "halt": return None
 
    status = self.send_intro_instructions(message)
    if status == "halt": return None

    return True

  def topup_request(self, message):
    credits = self.parse_message_credits(message.message)
    if credits == None: return "continue" #not a topup request
    self.send_message(message.customer, "You have offered to add " + credits + " credits to the power strip. Confirm by sending \"Yes\"")
    message.customer.status_value = str(credits)
    message.customer.status = "topup_offered"
    session.commit()
    return "halt"

  def confirm_topup_request(self, message):
    if message.customer.status!="topup_offered": return "continue"
    if re.search("[Y|y][E|e][S|s]", message.message):
      latest_meter_state = MeterState.latest()
      status_value = message.customer.status_value
      new_balance = latest_meter_state.balance + float(status_value)
      session.add(MeterState(balance=new_balance, action="topup"))
      message.customer.status = "active"
      message.customer.status_value = None
      self.send_message(message.customer, "You have added " + status_value + " credits to the power strip.")
      session.commit()

      return "halt"
    else:
      self.send_message(message.customer, "Topup declined. To add credit to the power strip, text 'ADD 100' to this number.")
      message.customer.status_value = None
      session.commit()
      return "halt"

  def process_balance_request(self, message):
    parsed = re.search("bal", message.message)
    if parsed == None : return "continue"
    #TODO: Send the current balance, with a suggestion for what to top up
    #TODO: Make no change to the current status
    return "halt"

  def send_intro_instructions(self, message):
    if(message.customer.status!="new"): return "continue"
    self.send_message(message.customer, "This is Grassroots Mobile Power. To add credit to the power strip, text 'ADD 100' to this number.")
    session.commit()
    return "halt"

  def parse_message_credits(self, message):
    parsed = re.search("[A|a][D|d][D|d] ([0-9].*)", message)
    if parsed == None: return None
    credits = parsed.group(1)
    return credits

  ## if the customer is new and the message isn't a topup request
  ## then send them information about the service
  ## NOTE: Does not commit the message to the db
  def send_message(self, customer, message):
    #TODO: ACTUALLY SEND THE MESSAGE
    customer = session.merge(customer)
    outgoing_message = OutgoingMessage(customer = customer, message = message)
    session.add(outgoing_message)
    session.commit()
    return outgoing_message

