from data_objects import *
import re

class MessagePipelineController:

  def check_messages(self):
    return None

  #pipeline items which return "continue" pass through
  #pipeline items which return "halt" halt the queue
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
    message.customer.status = "topup_offered"
    session.commit()
    #TODO: Store the proposed credit value somewhere
    return "halt"

  def confirm_topup_request(self, message):
    if message.customer.status!="topup_offered": return "continue"
    if re.search("[Y|y]", message.message):
      #TODO: TAKE ACTION TO ADD CREDITS
      #TODO: Set customer status to "active"
      #TODO: Send confirmation of topup, including the current balance
      return "halt"
    else:
      #TODO: send "Top up not confirmed. Try again"
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
    return "halt"

  def parse_message_credits(self, message):
    parsed = re.search("[A|a][D|d][D|d] ([0-9].*)", message)
    if parsed == None: return None
    credits = parsed.group(1)
    return credits

  ## if the customer is new and the message isn't a topup request
  ## then send them information about the service

  def send_message(self, customer, message):
    #TODO: ACTUALLY SEND THE MESSAGE
    customer = session.merge(customer)
    outgoing_message = OutgoingMessage(customer = customer, message = message)
    session.add(outgoing_message)
    session.commit()

