from data_objects import *
import re

class MessagePipelineController:

  def check_messages(self):
    [self.process_message(msg) for msg in session.query(IncomingMessage).filter_by(handled=False).order_by(asc(IncomingMessage.created))]
    return None

  #pipeline items which return "continue" pass through
  #pipeline items which return "halt" halt the queue
  #TODO: mark message as handled
  def process_message(self, message):
    status = self.confirm_topup_request(message)
    if status == "halt": 
      message.set_handled()
      return True

    status = self.topup_request(message)
    if status == "halt": 
      message.set_handled()
      return True
 
    status = self.process_balance_request(message)
    if status == "halt": 
      message.set_handled()
      return True
 
    status = self.send_intro_instructions(message)
    if status == "halt": 
      message.set_handled()
      return True

    return False

  def topup_request(self, message):
    credits = self.parse_message_credits(message.message)
    if credits == None: return "continue" #not a topup request
    self.send_message(message.customer, "You have offered to add " + credits + " credits to the power strip. Confirm by sending \"Yes\"")
    message.customer.status_value = str(credits)
    if(message.customer.status == "active"):
      message.customer.status = "topup_offered_active"
    else:
      message.customer.status = "topup_offered_inactive"
    session.commit()
    return "halt"

  def confirm_topup_request(self, message):
    if re.search("topup_offered", message.customer.status) == None: return "continue"
    if re.search("[Y|y][E|e][S|s]", message.message):
      latest_meter_state = MeterState.latest()
      status_value = message.customer.status_value
      new_balance = latest_meter_state.balance + float(status_value)
      session.add(MeterState(balance=new_balance, action="topup"))
      message.customer.status = "active"
      message.customer.status_value = None
     
      #TODO: Add a test for this
      #If the power is off, turn it on
      latest_command = SwitchCommand.latest()
      if(latest_command == None or (latest_command and latest_command.command!="on")):
        session.add(SwitchCommand(command="on"))

      session.commit()
      self.send_message(message.customer, "You have added " + status_value + " credits to the power strip.")

      return "halt"
    else:
      self.send_message(message.customer, "Topup successfully declined. To add credit to the power strip, text 'ADD 100' to this number.")
      message.customer.status_value = None
      if(message.customer.status == "topup_offered_active"): message.customer.status = "active"
      if(message.customer.status == "topup_offered_inactive"): message.customer.status = "inactive"

      return "halt"

  #only active customers may ask for the current balance
  def process_balance_request(self, message):
    parsed = re.search("[B|b][A|a][L|l]", message.message)
    if parsed == None : return "continue"
    if message.customer.status != "active": 
      self.send_message(message.customer, "Only current customers can check the balance. To add credit to the power strip, text 'ADD 100' to this number.")
      return "halt"
    balance = MeterState.latest().balance
    consumption = Consumption.latest()
    kilowatt_minutes_used = consumption.total_consumed
    credits_used = consumption.credits_used()
    credits_remaining = balance - credits_used
    paid_kilowatt_minutes = consumption.credits_to_kilowatt_minutes(balance)
    kilowatt_minutes_remaining = paid_kilowatt_minutes - kilowatt_minutes_used
    
    self.send_message(message.customer, "Current balance: " + str(credits_remaining) + " credits remaining. " + str(kilowatt_minutes_used) + " kilowatt-minutes used. " + str(kilowatt_minutes_remaining) + " kilowatt-minutes remaining. To add credit to the power strip, text 'ADD 100' to this number.")
    return "halt"

  def send_intro_instructions(self, message):
    if(message.customer.status!="new"): return "continue"
    self.send_message(message.customer, "This is Grassroots Mobile Power. To add credit to the power strip, text 'ADD 100' to this number.")
    return "halt"

  def parse_message_credits(self, message):
    parsed = re.search("[A|a][D|d][D|d] ([0-9].*)", message)
    if parsed == None: return None
    credits = parsed.group(1)
    return credits

  ## if the customer is new and the message isn't a topup request
  ## then send them information about the service
  ## NOTE: Does not commit the message to the db
  def send_message(self,customer, message):
    #TODO: ACTUALLY SEND THE MESSAGE
    customer = session.merge(customer)
    outgoing_message = OutgoingMessage(customer = customer, message = message)
    session.add(outgoing_message)
    session.commit()
    return outgoing_message

