from serial import Serial
import serial
import time
from functions import *
from gadi import *

functime = 7
refreshint = 4
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
	printtoarduino(arduino, "Since Surgery:", dayssince(date(2020,12,9)))
	time.sleep(refreshint)

	# printtoarduino(arduino, "Thesis Due:", daysuntil(date(2021,11,5)))
	# time.sleep(refreshint)

	# printtoarduino(arduino, "M/Y Report Due:", daysuntil(date(2021,8,20)))
	# time.sleep(refreshint)

	printtoarduino(arduino, "Lit Review Due:", daysuntil(date(2021,4,30)))
	time.sleep(refreshint)

	printtoarduino(arduino, "Gadi K96 KSU", gadiusageproject())
	time.sleep(refreshint)

	# printtoarduino(arduino, "Gadi " + str(printgadiusername()) + " KSU", gadiusageme())
	# time.sleep(refreshint)

	# filled, avail = gadiusagebar()
	# printtoarduino(arduino, "Gadi avail " + str(avail), usagebar(filled, 16))
	# time.sleep(refreshint)

	# printtoarduino(arduino, "Gadi Home Usage", gadihomequota())
	# time.sleep(refreshint)