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

	packet = bytearray()
	for i in range(32):
		j = printstring[i]
		packet.append(HD44780[j])

	arduino.write(packet)

# Simple running of bash commands 
def runbash(command):
    output = subprocess.run(command, stdout=subprocess.PIPE, shell=True).stdout.strip()
    if output != "":
        return(output.decode("utf-8"))

def cpupower():
	volts = subprocess.check_output("sensors k10temp-pci-00c3 | grep 'Vcore:' | tr -s ' '", shell=True)
	volts = volts.decode("utf-8").split()

	if volts[2] == "V":
		numvolts = float(volts[1])
	if volts[2] == "mV":
		numvolts = float(volts[1]) / 1000

	amps = subprocess.check_output("sensors k10temp-pci-00c3 | grep 'Icore:' | tr -s ' ' | cut -d' ' -f 2", shell=True)
	amps = amps.decode("utf-8")

	return(	str(round(numvolts * float(amps), 2)) + "W")

HD44780 = {" " : 0x20, "A" : 0x41, "B" : 0x42, "C" : 0x43, "D" : 0x44,
		   "E" : 0x45, "F" : 0x46, "G" : 0x47, "H" : 0x48, "I" : 0x49, 
		   "J" : 0x4A, "K" : 0x4B, "M" : 0x4D, "O" : 0x4F, "P" : 0x50,
		   "Q" : 0x51, "R" : 0x52, "S" : 0x53, "T" : 0x54, "U" : 0x55, 
		   "V" : 0x56, "W" : 0x57, "X" : 0x58, "Y" : 0x59, "Z" : 0x5A,
		   "a" : 0x61, "b" : 0x62, "c" : 0x63, "d" : 0x64, "e" : 0x65, 
		   "f" : 0x66, "g" : 0x67, "h" : 0x68, "i" : 0x69, "j" : 0x6A,
		   "k" : 0x6B, "l" : 0x6C, "m" : 0x6D, "n" : 0x6E, "o" : 0x6F, 
		   "p" : 0x70, "q" : 0x71, "r" : 0x72, "s" : 0x73, "t" : 0x74,
		   "u" : 0x75, "v" : 0x76, "w" : 0x77, "x" : 0x78, "y" : 0x79, 
		   "z" : 0x7A, "0" : 0x30, "1" : 0x31, "2" : 0x32, "3" : 0x33,
		   "4" : 0x34, "5" : 0x35, "6" : 0x36, "7" : 0x37, "8" : 0x38,
		   "9" : 0x39, "!" : 0x21, "\"" : 0x22, "#" : 0x23, "$" : 0x24,
		   "%" : 0x25, "&" : 0x26, "'" : 0x27, "(" : 0x28, ")" : 0x29,
		   "*" : 0x2A, "+" : 0x2B, "," : 0x2C, "-" : 0x2D, "." : 0x2E,
		   "/" : 0x2F, ":" : 0x3A, ";" : 0x3B, "<" : 0x3C, "=" : 0x3D,
		   ">" : 0x3E, "?" : 0x3F, "@" : 0x40, "[" : 0x5B, "]" : 0x5D,
		   "^" : 0x5E, "_" : 0x5F, "`" : 0x60, "{" : 0x7B, "|" : 0x7C,
		   "}" : 0x7D, "→" : 0x7E, "←" : 0x7F, "·" : 0x85, "°" : 0xDF,
		   "█" : 0xFF, "~" : 0xB0}
