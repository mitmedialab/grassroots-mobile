from data_objects import *
from message_pipeline_controller import *
import re

class BusinessLogicController:
  # return true if it takes some kind of action
  def process_consumption_report(self, consumption):
    meter_state = MeterState.latest()
    #TODO: test the following line
    # Rule: ignore all consumption reports ecxept in cases where there is credit
    if(meter_state.action!="topup"): return False
    kilowatt_minutes_funded = consumption.credits_to_kilowatt_minutes(meter_state.balance)
    mpc = MessagePipelineController()

    if(consumption.total_consumed > kilowatt_minutes_funded):
      session.add(SwitchCommand(command="off"))
      session.add(MeterState(balance=0.0, action="shutdown"))
      for customer in Customer.active_customers():
        customer.status="inactive"
        customer.status_value=None
      session.commit()
      return True

    if(consumption.total_consumed > kilowatt_minutes_funded*0.75):
      credits_remaining = meter_state.balance - consumption.credits_used()
      for customer in Customer.active_customers():
        mpc.send_message(customer, "There are " + str(credits_remaining) + " credits remaining on the power strip. You have used " + str(consumption.credits_used()) + " credits, a total of " + str(consumption.total_consumed)  + " kilowatt-minutes. To add credit to the power strip, text 'ADD 100' to this number.")
      return True
    return False
