#!/bin/bash
while [ ! -c /dev/ttyUSB0 ]
do
	echo 'waiting for the msp430...'
	sleep 1s
done
python pwsw-daemon.py


