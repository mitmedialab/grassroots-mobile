from data_objects import *
from readsms import *
from sendsms import *
import time

sleep_time = 2
mpc = MessagePipelineController()
port = '/dev/gsm1'
dbsession = Session()

while(1):
    #Check for any unread messages
    smslist = readsms(port,'unread')
    for sms in smslist:
        customer = sms['customer']
        contents = sms['contents']
        sms_timestamp = sms['timestamp']

        #find/create/update an existing customer with this customer id
        customer_object = dbsession.query(Customer).filter_by(msisdn=customer).first()
        if customer_object == None:
            customer_object = Customer(msisdn=customer,status="new")
            dbsession.add(customer)
        else:
            customer_object.status = "active"
            dbsession.merge(customer_object)
        
        #create a new message object
        incoming_msg_object = IncomingMessage(customer = customer_object,message = contents, created = sms_timestamp)
        dbsession.add(incoming_msg_object)
        mpc.process_message(incoming_msg_object)
        dbsession.commit()

    #Check for any messages to be sent out
    outgoing_msgs = dbsession.query(OutgoingMessage).filter_by(handled=False).all()
    for msg in outgoing_msgs:
        customer_no = msg.customer.msisdn
        msg_text = msg.message_template.text
        sendsms(port,customer_no,msg_text)
        msg.handled = True
        dbsession.merge(msg)
        dbsession.commit()

    #just sleep very very peacfully for exactly <sleep_time> seconds
    time.sleep(sleep_time)
        

