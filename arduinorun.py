import subprocess
from serial import Serial
import serial
import time
from functions import *
import binascii

functime = 5

arduino = Serial('/dev/tty.usbmodem1414201', 115200, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)
time.sleep(2)

# Master loop. loops thorugh all of the sub functions of the display
while True:

	# simple cpu meter, 
	endtime = time.time() + functime
	procmult = int(runbash('nproc'))*100

	while endtime > time.time():
		usage = int(round(16 * (float(runbash("ps -e -o %cpu | awk '{s+=$1} END {print s}'"))/procmult), 0))
		usagebar = ''
		for i in range(usage):
			usagebar = usagebar + '#'

		printtoarduino(arduino, "CPU utilisation:", usagebar)
		time.sleep(0.5)

	# simple cpu temp meter
	endtime = time.time() + functime
	while endtime > time.time():
		cputemp = runbash('sudo powermetrics --samplers smc -i1 -n1 | grep "CPU die" | cut -d " " -f 4')
		printtoarduino(arduino, "CPU Temperature:", cputemp)
