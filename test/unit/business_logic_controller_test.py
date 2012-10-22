import unittest
from business_logic_controller import *
from message_pipeline_controller import *
from data_objects import *
import test_common 

class BusinessLogicControllerTest(unittest.TestCase):
  def setUp(self):
    self.customers = [Customer(msisdn="123456789012345", status="new"),
                      Customer(msisdn="223456789012345", status="active"),
                      Customer(msisdn="223456789012345", status="active"),
                      Customer(msisdn="223456789012345", status="topup_offered_active")]
    [session.add(customer) for customer in self.customers]
    session.commit()
    return None
   
  def tearDown(self):
    [session.delete(customer) for customer in session.query(Customer).all()]
    [session.delete(message) for message in session.query(OutgoingMessage).all()]
    [session.delete(state) for state in session.query(MeterState).all()]
    [session.delete(consumption) for consumption in session.query(Consumption).all()]
    session.commit()
    return None

  def testProcessConsumptionReport(self):
    meter_state = MeterState(balance=100.0, action="started")
    consumption = Consumption(total_consumed=50.0, consumed_since_last_report=20.0)
    session.add(meter_state)
    session.add(consumption)
    session.commit()
   
    blc = BusinessLogicController()

    ## assert no action taken when consumed is too low
    self.assertFalse(blc.process_consumption_report(consumption))
   

    ##customers notified when consumed passes the notification threshhold
    consumption = Consumption(total_consumed=80.0, consumed_since_last_report=30.0)
    session.add(consumption)
    session.commit()
    self.assertEqual(0, len(session.query(OutgoingMessage).all()))
    self.assertTrue(blc.process_consumption_report(consumption))
    self.assertEqual("There are 20.0 credits remaining on the power strip. You have used 80.0 credits, a total of 80.0 kilowatt-minutes. To add credit to the power strip, text 'ADD 100' to this number.", session.query(OutgoingMessage).all()[-1].message)
    self.assertEqual(3, len(session.query(OutgoingMessage).all()))
   
    consumption = Consumption(total_consumed=101.0, consumed_since_last_report=21.0)
    session.add(consumption)
    session.commit()
    self.assertTrue(blc.process_consumption_report(consumption))
    meter_state = MeterState.latest()
    self.assertEqual(0.0, meter_state.balance)
    self.assertEqual("shutdown", meter_state.action)
    self.assertEqual(0, len(Customer.active_customers().all()))

    #debug line, for further reference
    #import pdb; pdb.set_trace()


test_common.ALL_TESTS.append(BusinessLogicControllerTest)

if __name__ == '__main__':
  unittest.main()
