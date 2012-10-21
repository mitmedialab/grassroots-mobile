from data_objects import *
import re

class MessagePipelineController:

  def check_messages(self):
    return None

  #pipeline items which return "continue" pass through
  #pipeline items which return "halt" halt the queue
  def process_message(self, message):
    status = self.confirm_topup_request(message)
    status = self.topup_request(message)
    status = self.process_balance_request(message)
    return None

  def topup_request(self, message):
    credits = self.parse_message_credits(messsage)
    if credits == None: return "continue" #not a topup request
    #TODO: Store the proposed credit value somewhere
    #TODO: Set customer status "topup_offered"
    #TODO: Send and log Outgoing confirmation message
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
    parsed = re.search("bal", message)
    if parsed == None : return "continue"
    #TODO: Send the current balance, with a suggestion for what to top up
    #TODO: Make no change to the current status
    return "halt"

  def parse_message_credits(self, message):
    parsed = re.search("[A|a][D|d][D|d] ([0-9].*)", message)
    if parsed == None: return None
    credits = parsed.group(1)
    return credits

  def send_fake_message(self, customer, message):
    outgoing_message = OutgoingMessage(customer = customer, message = message)
    self.session.add(outgoing_message)
    self.session.commit()

