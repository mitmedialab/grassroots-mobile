import serial, sys

def sendsms(port,number,text):
    port = serial.Serial(port, 115200, timeout=2)
    port.flushInput()
    port.flushOutput()

    #just send an AT
    port.write('AT\r\n')
    line = port.readline()
    port.readline()

    #set format
    command = 'AT+CMGF=1\r\n'
    port.write(command)
    port.readline()
    #port.readline()

    #send send message command
    command = 'AT+CMGS=%s\r\n'%(number.__str__())
    #print command
    port.write(command)
    port.readline()
    #port.readline()
    
    #send text
    port.write(text)
    port.write('\r\n')
    #send control-x
    port.write('\x1A')
    print 'SendSMS debug'
    #print port.readline()
    #print port.readline()
    #print port.readline()

