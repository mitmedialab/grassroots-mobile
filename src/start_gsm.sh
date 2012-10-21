#!/bin/bash
while [ ! -c /dev/gsm1 ]
do
	echo 'waiting for the gsm device...'
	sleep 1s
done
python sms-daemon.py


