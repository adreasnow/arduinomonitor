import subprocess
import time

# prints to the arduino over serial
def printtoarduino(arduino, line1, line2):
	# pads the lines to ensure line2 is forced on to the second line 
	# and the cursor is forced off the screen, since \r and \n don't seem to work
	line1len = len(line1)
	line2len = len(line2)
	line1pad = 16 - line1len
	line2pad = 16 - line2len
	line1padstr = ''
	line2padstr = ''
	for i in range(line1pad):
		line1padstr = line1padstr + ' '
	for i in range(line2pad):
		line2padstr = line2padstr + ' '
	printstring = line1[0:16] + line1padstr + line2[0:16] + line2padstr
	arduino.write((printstring).encode('ascii'))

# Simple running of bash commands 
def runbash(command):
    output = subprocess.run(command, stdout=subprocess.PIPE, shell=True).stdout.strip()
    if output != "":
        return(output.decode("utf-8"))