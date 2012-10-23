import serial, sys, time
from numpy import *
from data_objects import *
from business_logic_controller import *

port = '/dev/ttyUSB0'
ser = serial.Serial(port, 230400, timeout=5)
#f = open('serlog','w')
p1 = 0.0732
p2 = -15.69

#poll db every <> samples
poll_db_interval = 1000
sample_count = 0
energy_consumed = 0.0
consumed_since_last_report = 0.0

def switch_off(ser):
    ser.write('f')

def switch_on(ser):
    ser.write('t')

def delWattMin(power,deltime):
    seconds = (deltime.days*86400)+deltime.seconds+(float(deltime.microseconds)/1000000)
    minutes = seconds/60
    return minutes * power


class RingArray(object):
    def __init__(self,size):
        self.inarray = zeros(size,dtype=int16)
        self.size = size
        self.pointer = 0 #This is where the array starts at
    
    def insert(self,p):
        #You insert the element where the array started at, and 
        #move the pointer one step ahead
        oldElem = self.inarray[self.pointer]
        self.inarray[self.pointer] = p
        self.pointer = (self.pointer + 1)%self.size
        self.update(oldElem,p)



class AvgRingArray(RingArray):
    def __init__(self,size):
        super(AvgRingArray,self).__init__(size)
        self.value = 0
        self.count = 0
        for i in self.inarray:
            self.value += float(i)/self.size
    
    def scratch(self):
        self.value = 0
        for i in self.inarray:
            self.value += float(i)/self.size

    def update(self,ejectedElem,newElem):
        #print 'e %d n %d'%(ejectedElem,newElem)
        self.count += 1
        if self.count >= 200:
            self.scratch()
            self.count = 0
        else:
            self.value = float(self.value) - float(ejectedElem)/self.size + float(newElem)/self.size


current_bias = AvgRingArray(500)
voltage_bias = AvgRingArray(500)
power_avg = AvgRingArray(1200)
dbsession = Session()
lastttime = None

blc = BusinessLogicController()

while True:
    line = ser.readline()
    a =  line.split()
    if len(a) > 1:
        current_biased = int(a[0])
        voltage_biased = int(a[1])
        voltage_bias.insert(voltage_biased)
        current_bias.insert(current_biased)
        voltage_unbiased = voltage_biased-voltage_bias.value
        current_unbiased = current_biased-current_bias.value
        power = p1*(abs(voltage_unbiased * current_unbiased))+p2
        power_avg.insert(power)
        
        #this part calculates the total energy used
        if lasttime is not None:
            nowtime = datetime.datetime.now()
            deltime = nowtime - lasttime
            lasttime = nowtime
            delEnergy = delWattMin(power_avg.value,deltime)
            energy_consumed = energy_consumed + delEnergy
            consumed_since_last_report = consumed_since_last_report + delEnergy
        else:
            lasttime = datetime.datetime.now()


        sample_count = (sample_count + 1)%poll_db_interval

        if sample_count == 0:
            #check db if we need to flip the switch
            shutoff_cmd = dbsession.query(ShutoffCommand).filter_by(handled=False).order_by(desc(ShutoffCommand.id)).first()
            if shutoff_cmd is not None:
                if shutoff_cmd.command == 'off':
                    switch_off(ser)
                    shutoff_cmd.handled = True
                    dbsession.merge(shutoff_cmd)
                    dbsession.commit()
                    energy_consumed = 0
                    consumed_since_last_report = 0

                if shutoff_cmd.command == 'on':
                    switch_on(ser)
                    shutoff_cmd.handled = True
                    dbsession.merge(shutoff_cmd)
                    dbsession.commit()
                    energy_consumed = 0
                    consumed_since_last_report = 0
                    
            else:
            #create a new consumed object
                cobj = Consumed(total_consumed = energy_consumed,
                                consumed_since_last_report = consumed_since_last_report)
                dbsession.add(cobj)
                dbsession.commit()
                consumed_since_last_report = 0
                blc.process_consumption_report(cobj)
            
        #print 'i',power
        #print '%0.1fwatts'%(power_avg.value)
        
