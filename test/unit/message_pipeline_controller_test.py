import unittest
from message_pipeline_controller import *
import test_common 

class MessagePipelineControllerTest(unittest.TestCase):
  def setUp(self):
    self.session = Session()
    self.pipeline = MessagePipelineController()
    self.messages = []
    self.outgoing = []
    self.customers = [Customer(msisdn="123456789012345", status="new")]
    self.session.add(self.customers[0])
    self.session.commit()
   
  #delete all messages and customers created for this test
  def tearDown(self):
    [self.session.delete(message) for message in self.messages]
    [self.session.delete(customer) for customer in self.customers]
    [self.session.delete(message) for message in self.session.query(OutgoingMessage).all()]
    self.session.commit()
    self.session.close()

  def outgoingCount(self):
    return len(self.session.query(OutgoingMessage).all())

  def testCheckMessages(self):
    return None 

  def testSendMessage(self):
    outgoing_message_count = self.outgoingCount()
    self.pipeline.send_message(self.customers[0], "The Ides of March")
    self.assertEqual("The Ides of March", self.session.query(OutgoingMessage).all()[-1].message)
    self.assertNotEqual(outgoing_message_count, self.outgoingCount())

  def receiveMessage(self, customer, message_text):
    message = IncomingMessage(message=message_text)
    self.messages.append(message)
    customer.incoming_messages.append(message)
    self.session.commit() 
    return message

  def lastSentMessage(self):
    return self.session.query(OutgoingMessage).all()[-1]

  def testProcessMessage(self):
    duff_message = self.receiveMessage(self.customers[0], "slartibartfast")
    
    # ensure that a duff message result in no action
    outgoing_message_count = self.outgoingCount()
    customer_status = self.customers[0].status
    self.pipeline.process_message(duff_message) 
    self.assertEqual(outgoing_message_count+1, self.outgoingCount())
    self.assertEqual("This is Grassroots Mobile Power. To add credit to the power strip, text 'ADD 100' to this number.", self.lastSentMessage().message)
    self.assertEqual(customer_status, self.customers[0].status)

    # receive a new message from a new customer
    outgoing_message_count = self.outgoingCount()
    add_credit_message = self.receiveMessage(self.customers[0], "ADD 100")
    self.assertEqual("new", self.customers[0].status)
    self.pipeline.process_message(add_credit_message)
    self.assertEqual(outgoing_message_count+1, self.outgoingCount())
    self.assertEqual("You have offered to add 100 credits to the power strip. Confirm by sending \"Yes\"", self.lastSentMessage().message)
    self.assertEqual("100", self.customers[0].status_value)
    self.assertEqual("topup_offered", self.customers[0].status)

    #debug line, for further reference
    #import pdb; pdb.set_trace()
    return None


test_common.ALL_TESTS.append(MessagePipelineControllerTest)

if __name__ == '__main__':
  unittest.main()