import unittest
import business_logic_controller
from message_pipeline_controller import *
from data_objects import *
import test_common 

class BusinessLogicControllerTest(unittest.TestCase):
  def setUp(self):
    return None
   
  def tearDown(self):
    return None

  def testSetupTeardown(self):
    return None

test_common.ALL_TESTS.append(BusinessLogicControllerTest)

if __name__ == '__main__':
  unittest.main()
