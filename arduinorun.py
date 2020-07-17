from serial import Serial
import serial
import time
from functions import *

functime = 5
arduino = Serial('/dev/ttyACM0', 115200, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)
time.sleep(2)


# Master loop. loops thorugh all of the sub functions of the display
while True:

	# cpu/gpu power meter
	endtime = time.time() + functime
	while endtime > time.time():
		cpupow = runbash('/data/Computation/Scripts/conky/conkywatts.py')
		gpupow = runbash("sensors | grep 'power1' | tr -s ' ' | cut -d' ' -f2") + "W"
		padding = ''
		for i in range(16 - len(cpupow + gpupow)):
			padding = padding + ' '
		printtoarduino(arduino, "CPU  -POWR-  GPU", cpupow + padding + gpupow)
		time.sleep(1)

	# cpu/gpu temp meter
	endtime = time.time() + functime
	while endtime > time.time():
		cputemp = runbash('sensors k10temp-pci-00c3 | grep "Tctl:" | tr -s " " | cut -d" " -f 2')
		gputemp = runbash("sensors | grep 'edge:' | tr -s ' ' | cut -d' ' -f 2")
		printtoarduino(arduino, "CPU  -TEMP-  GPU", cputemp + "  " + gputemp)
		time.sleep(1)

	# cpu/gpu usage meter, 
	endtime = time.time() + functime
	procmult = int(runbash('nproc'))*100
	while endtime > time.time():
		usage = int(round(11 * (float(runbash("ps -e -o %cpu | awk '{s+=$1} END {print s}'"))/procmult), 0))
		usagebarcpu = ''
		for i in range(usage):
			usagebarcpu = usagebarcpu + '█'
		percentage = int(runbash("/opt/radeontop/radeontop -d- -l1 | grep -o 'gpu [0-9]\{1,3\}' | cut -c 5-7"))
		usage = round((percentage/100)*11)
		usagebargpu = ''
		for i in range(usage):
			usagebargpu = usagebargpu + '█'

		printtoarduino(arduino, "CPU: " + usagebarcpu, "GPU: " + usagebargpu, )
		time.sleep(0.2)

	# mem usage meter
	endtime = time.time() + functime
	while endtime > time.time():
		total = float(runbash('cat /proc/meminfo | grep "MemTotal:" | tr -s " " | cut -d" " -f2'))
		avail = float(runbash('cat /proc/meminfo | grep "MemAvailable:" | tr -s " " | cut -d" " -f2'))
		usage = round(((total - avail)/total)*16)
		usagebar = ''
		for i in range(usage):
			usagebar = usagebar + '█'

		printtoarduino(arduino, "Mem utilisation:", usagebar)
		time.sleep(0.5)



	printtoarduino(arduino, "CPU Governor:", runbash("/data/Computation/Scripts/conky/conkygov.sh"))
	time.sleep(3)

	