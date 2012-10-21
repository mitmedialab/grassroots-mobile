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
    self.session.add(customers[0])
    self.session.commit()
   
  #delete all messages and customers created for this test
  def tearDown(self):
    [self.session.delete(message) for message in self.messages]
    [self.session.delete(customer) for customer in self.customers]
    [self.session.delete(message) for message in self.session.query(OutgoingMessages).all()]
    self.session.commit()
    self.session.close()

  def testCheckMessages(self):
    return None 

  def testSendFakeMessage(self):
    outgoing_message_count = self.outgoingCount()
    self.pipeline.send_fake_message(self.customers[0], "The Ides of March")
    assertEqual("The Ides of March", self.session.query(OutgoingMessages).all()[-1].message)
    assertNotEqual(outgoing_message_count, self.outgoingCount())

  def testProcessMessage(self):
    duff_message = IncomingMessage(message="slartibartfast")
    self.messages.append(duff_message)
    self.customers[0].incoming_messages.append(duff_message)
    self.session.commit() #message added
    
    # ensure that a duff message result in no action
    outgoing_message_count = self.outgoingCount()
    customer_status = self.customers[0].status
    self.pipeline.process_message(incoming_message) 
    assertEqual(outgoing_message_count, self.outgoingCount())
    assertEqual(customer_status, self.customers[0].status)

    #debug line, for further reference
    #import pdb; pdb.set_trace()
    return None

    def outgoingCount(self):
      return len(self.session.query(OutgoingMessage).all())

test_common.ALL_TESTS.append(MessagePipelineController)

if __name__ == '__main__':
  unittest.main()
