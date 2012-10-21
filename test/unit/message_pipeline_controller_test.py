import unittest
from message_pipeline_controller import *
import test_common 

class MessagePipelineControllerTest(unittest.TestCase):
  def setUp(self):
    self.session = Session()
    self.pipeline = MessagePipelineController()
    self.messages = []
    self.customers = [Customer(msisdn="123456789012345", status="new")]
    self.session.add(customers[0])
    self.session.commit()
   
  #delete all messages and customers created for this test
  def tearDown(self):
    [self.session.delete(message) for message in self.messages]
    [self.session.delete(customer) for customer in self.customers]
    self.session.commit()
    self.session.close()

  def testCheckMessages(self):
    return None 

  def testProcessMessage(self):
    duff_message = IncomingMessage(message="slartibartfast")
    self.messages.append(duff_message)
    self.customers[0].incoming_messages.append(duff_message)
    self.session.commit() #message added
    
    outgoing_message_count = self.outgoingCount()
    self.pipeline.process_message(incoming_message) 
    assertEqual(outgoing_message_count, self.outgoingCount())
    

    #debug line, for further reference
    #import pdb; pdb.set_trace()
    return None

    def outgoingCount(self):
      return len(self.session.query(OutgoingMessage).all())

test_common.ALL_TESTS.append(MessagePipelineController)

if __name__ == '__main__':
  unittest.main()
