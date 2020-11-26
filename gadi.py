import subprocess
from functions import *
import time
from datetime import datetime, timedelta, date

global allocation
global gadifrequency
global gadiusername
global gadi_reserved_me
gadiusername = "fhh565"
gadifrequency = 300
gadi_reserved_me = "960.00"

global gadiusageruntime
global gadi_grant_project
global gadi_used_project
global gadi_reserved_project
global gadi_avail_project
global gadi_used_me
global gadi_avail_me
global gadihomequotaruntime
global gadi_homequota

def msu2ksu(value, string):
	if string == 'MSU':
		value = float(value) * 1000
	else:
		value = value
	return(str(value))

def getgadiusage():
	def sshcall():
		gadioutput = runbash("ssh as1892@gadi.nci.org.au \"nci_account -v\"").splitlines()
		globals()['gadi_grant_project'] = msu2ksu(gadioutput[2].split()[1], gadioutput[2].split()[2])
		globals()['gadi_used_project'] = msu2ksu(gadioutput[3].split()[1], gadioutput[3].split()[2])
		globals()['gadi_reserved_project'] = msu2ksu(gadioutput[4].split()[1], gadioutput[4].split()[2])
		globals()['gadi_avail_project'] = msu2ksu(gadioutput[5].split()[1], gadioutput[5].split()[2])
		for i in range(0, len(gadioutput) - 2):
			if globals()['gadiusername'] in gadioutput[i]:
				globals()['gadi_used_me'] = msu2ksu(gadioutput[i].split()[1], gadioutput[i].split()[2])
				str(globals()['gadi_avail_me']) = float(globals()['gadi_reserved_me']) - float(globals()['gadi_used_me'])
		print("ssh call")
	if 'gadiusageruntime' in vars() or 'gadiusageruntime' in globals():
		timesince = time.time() - globals()['gadiusageruntime']
		if timesince > globals()['gadifrequency']:
			sshcall()
			globals()['gadiusageruntime'] = time.time()

	else:
		sshcall()
		globals()['gadiusageruntime'] = time.time()


def gadiusageproject():
	getgadiusage()
	return(globals()['gadi_avail_project'] + "/" + globals()['gadi_grant_project'])


def gadiusageme():
	getgadiusage()
	return(globals()['gadi_used_me'] + "/" + globals()['gadi_avail_me'])


def getgadihomequota():
	gadioutput = runbash("ssh as1892@gadi.nci.org.au \"du -hs ~\"")
	print("ssh call")
	return(gadioutput)	

def gadihomequota():
	if 'gadihomequotaruntime' in vars() or 'gadihomequotaruntime' in globals():
		timesince = time.time() - globals()['gadihomequotaruntime']
		if timesince > globals()['gadifrequency']:
			globals()['gadi_homequota'] = getgadihomequota().split()[0]
			globals()['gadihomequotaruntime'] = time.time()

	else:
		globals()['gadi_homequota'] = getgadihomequota().split()[0]
		globals()['gadihomequotaruntime'] = time.time()

	return(globals()['gadi_homequota'] + "/10G")

for i in range(200):
	print(gadiusageproject())
	print(gadiusageme())
	print(gadihomequota())

	time.sleep(3)

