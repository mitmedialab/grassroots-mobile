import serial, sys, datetime

typedict = {
    'unread':'REC UNREAD',
    'read' : 'REC READ',
    'all' : 'ALL'
}

def sms(index,customer,time,date,msg):
    a = {}
    a['index'] = index.__str__()
    a['customer'] = customer.__str__()
    a['time'] = time.__str__()
    a['date'] = date.__str__()
    tmp1 = a['date'] + ' ' + a['time']
    tmp2 = tmp1.split('-')[0]
    a['timestamp'] = datetime.datetime.strptime(tmp2,'"%d/%m/%y %H:%M:%S')
    a['contents'] = msg.__str__()
    return a


def readsms(port,a):
    smslist = []
    port = serial.Serial(port, 115200, timeout=5)
    port.flushInput()
    port.flushOutput()
    port.write('AT\r\n')
    #print 1,port.readline()
    #print 2,port.readline()
    port.write('AT+CMGF=1\r\n')
    #print 1,port.readline()
    #print 2,port.readline()
    port.flushOutput()
    port.flushInput()
    port.write('AT+CMGL="%s"\r\n'%(typedict[a]))  #get all messages 
    inside_cmgl_output = False
    while(1):
        line = port.readline()
        print 'debug:',line
        if line.startswith('BOOT'):
            print 'ignoring crap'
            break
        if line.startswith('MODE'):
            print 'ignoreing crap'
            break
        if line.startswith('^BOOT'):
            print 'ignoring crap'
            break
        if line.startswith('^MODE'):
            print 'ignoreing crap'
            break

        if line.startswith('AT+CMGL='):
            inside_cmgl_output = True
            continue
        if line.startswith('+CMGL'):
            info = line.split(',')
            index = info[0].split(':')[1]
            customer = info[2]
            date = info[5]
            time = info[4]
            msg = port.readline()
            print 'message#%s from %s date %s time %s %s'     \
                %(index,customer,date,time,msg)
            a = sms(index,customer,date,time,msg)
            smslist.append(a)
            gotmsg = True
        if inside_cmgl_output and line.startswith('OK'):
            break
    return smslist

