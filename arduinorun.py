from serial import Serial
import serial
import time
from functions import *

functime = 5
arduino = Serial('/dev/ttyACM0', 115200, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)
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
			usagebar = usagebar + '█'

		printtoarduino(arduino, "CPU utilisation:", usagebar)
		time.sleep(0.5)

	# simple cpu temp meter
	endtime = time.time() + functime
	while endtime > time.time():
		cputemp = runbash('sensors k10temp-pci-00c3 | grep "Tctl:" | tr -s " " | cut -d" " -f 2')
		printtoarduino(arduino, "CPU Temperature:", cputemp)
		time.sleep(1)

	printtoarduino(arduino, "CPU Governor:", runbash("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor"))
	time.sleep(3)