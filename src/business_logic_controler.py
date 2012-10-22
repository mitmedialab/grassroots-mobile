from data_objects import *
import re

class BusinessLogicController:
  def process_consumption_report(self, consumption):
    meter_state = MeterState.latest()
    kilowatt_minutes_funded = Consumption.credits_to_kilowatt_minutes(meter_state.balance)


    if(consumption.total_consumed > kilowatt_minutes_funded):
      print "shut off kilowatt"
      ##TODO: Shut Off Kilowatt
      ##TODO: Log it in whatever way seems sensible

    if(consumption.total_consumed > kilowatt_minutes_funded*0.75):
      active_customers = Customer.active_customers()
      ##TODO: notify everyone who's an active customer

    return None
