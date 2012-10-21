from data_objects import *
from readsms import *
from sendsms import *
import time

sleep_time = 2

while(1):
    #Check for any messages to be sent out

    #Check for any unread messages
    smslist = readsms('/dev/ttyUSB1','unread')
    for sms in smslist:
        dbsession = Session()
        customer = sms['customer']
        contents = sms['contents']
        sms_timestamp = sms['timestamp']

        #find/create/update an existing customer with this customer id
        customer_object = dbsession.query(Customer).find_by(msisdn=customer).first()
        if customer_object == None:
            customer_object = Customer(msisdn=customer,status="new")
            dbsession.add(customer)
        else:
            customer_object.status = "active"
            dbsession.merge(customer_object)
        
        #create a new message object
        incoming_msg_object = IncomingMessage(customer = customer_object,message = contents, created = sms_timestamp)
        dbsession.add(incoming_msg_object)
        dbsession.commit()

    #just sleep very very peacfully for exactly <sleep_time> seconds
    time.sleep(sleep_time)
        

