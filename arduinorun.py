from serial import Serial
import serial
import time
from functions import *
from gadi import *

gadifrequency = 300

functime = 7
refreshint = 1
uname = runbash("uname")
if uname == "Linux":
	dev = runbash("ls /dev/ | grep 'ACM'")
	arduino = Serial('/dev/' + dev, 115200, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)
elif uname == "Darwin":
	dev = runbash("ls /dev/ | grep 'usbmodem' | grep 'tty'")
	arduino = Serial('/dev/' + dev, 115200, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)
time.sleep(2)


# Master loop. Loops thorugh all of the sub functions of the display
while True:
	printtoarduino(arduino, "Gadi Home Usage", "429.17K/269.81K")
	time.sleep(3)

	printtoarduino(arduino, "Surgery Wait:", daysuntil(date(2020,12,9)))
	time.sleep(3)

	printtoarduino(arduino, "Uni Left:", daysuntil(date(2020,12,1)))
	time.sleep(3)

	printtoarduino(arduino, "Gadi K96 (KSU)", gadiusageproject())
	time.sleep(3)

	printtoarduino(arduino, "Gadi My (KSU)", gadiusageme())
	time.sleep(3)

	filled = float(globals()['gadi_used_me'])/float(globals()['gadi_avail_me']) * 16

	printtoarduino(arduino, "Gadi avail " + globals()['gadi_avail_me'], usagebar(filled, 16))
	time.sleep(3)

	printtoarduino(arduino, "Gadi Home Usage", gadihomequota())
	time.sleep(3)

###################################### For rosalind #######################################
		# if uname == "Rosalind":
		# 	# cpu/gpu power meter
		# 	endtime = time.time() + functime
		# 	while endtime > time.time():
		# 		cpupow = cpupower()
		# 		gpupow = runbash("sensors | grep 'power1' | tr -s ' ' | cut -d' ' -f2") + "W"
		# 		printtoarduino(arduino, "CPU  -POWR-  GPU", cpupow + padding(cpupow + gpupow) + gpupow)
		# 		time.sleep(refreshint)

		# 	# cpu frequencies
		# 	endtime = time.time() + functime
		# 	while endtime > time.time():
		# 		cpulow, cpuhigh = cpufreq()
		# 		printtoarduino(arduino, "LOW  -FREQ- HIGH", cpulow + padding(cpuhigh + cpulow) + cpuhigh)
		# 		time.sleep(refreshint)

		# 	# cpu/gpu temp meter
		# 	endtime = time.time() + functime
		# 	while endtime > time.time():
		# 		cputemp = runbash('sensors k10temp-pci-00c3 | grep "Tctl:" | tr -s " " | cut -d" " -f 2')
		# 		gputemp = runbash("sensors | grep 'edge:' | tr -s ' ' | cut -d' ' -f 2")
		# 		printtoarduino(arduino, "CPU  -TEMP-  GPU", cputemp + "  " + gputemp)
		# 		time.sleep(refreshint)

		# 	# cpu/gpu usage meter, 
		# 	endtime = time.time() + functime
		# 	procmult = int(runbash('nproc'))*100
		# 	while endtime > time.time():
		# 		cpuusage = float(runbash("ps -e -o %cpu | awk '{s+=$1} END {print s}'"))/procmult
		# 		gpuusage = float(runbash("/opt/radeontop/radeontop -d- -l1 | grep -o 'gpu [0-9]\{1,3\}' | cut -c 5-7"))/100
		# 		usagebarcpu = usagebar(cpuusage, 12)
		# 		usagebargpu = usagebar(gpuusage, 12)

		# 		printtoarduino(arduino, "CPU:" + usagebarcpu, "GPU:" + usagebargpu, )
		# 		time.sleep(refreshint)

		# 	# mem usage meter
		# 	endtime = time.time() + functime
		# 	while endtime > time.time():
		# 		total = float(runbash('cat /proc/meminfo | grep "MemTotal:" | tr -s " " | cut -d" " -f2'))
		# 		avail = float(runbash('cat /proc/meminfo | grep "MemAvailable:" | tr -s " " | cut -d" " -f2'))
		# 		usage = usagebar(((total - avail)/total), 16)
		# 		printtoarduino(arduino, "Mem utilisation:", usage)
		# 		time.sleep(refreshint)

		# 	printtoarduino(arduino, "CPU Governor:", runbash("cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor").capitalize())
		# 	time.sleep(3)
