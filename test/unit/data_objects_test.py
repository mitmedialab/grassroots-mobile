import unittest
from data_objects import *
import test_common 

class DataObjectsTest(unittest.TestCase):
  def setUp(self):
    self.session = Session()
   
  def tearDown(self):
    self.session.close()

  def testObjectRelations(self):

    # test meter_state, just to make sure all is well
    meter_state = MeterState(balance=0.5, action="sample")
    self.session.add(meter_state)
    self.session.commit()
    self.assertNotEqual(meter_state.created, None)
    self.assertEqual(0.5, meter_state.balance)
    self.assertEqual("sample", meter_state.action)
    self.session.delete(meter_state)
    self.session.commit()

    customer = Customer(msisdn="123456789012345", status="active")
    incoming_message = IncomingMessage(message="ADD 100")
    customer.incoming_messages.append(incoming_message)
    self.session.add(customer)
    self.session.commit()
    self.session.delete(incoming_message)
    self.session.delete(customer)
    self.session.commit()
    
    #debug line, for further reference
    #import pdb; pdb.set_trace()

test_common.ALL_TESTS.append(DataObjectsTest)

if __name__ == '__main__':
  unittest.main()
