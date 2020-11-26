import subprocess
from functions import *
import time
from datetime import datetime, timedelta, date

global allocation
global gadifrequency
global gadiusername
gadiusername = "fhh565"
gadifrequency = 300
allocation = "340K"

global gadiusageruntime
global gadi_grant_project
global gadi_used_project
global gadi_reserved_project
global gadi_avail_project
global gadi_used_me
global gadi_reserved_me
global gadi_avail_me
global gadihomequotaruntime
global gadi_homequota

def getgadiusage():
	def sshcall():
		gadioutput = runbash("ssh as1892@gadi.nci.org.au \"nci_account -v\"").splitlines()
		globals()['gadi_grant_project'] = gadioutput[2].split()[1] + " " + gadioutput[2].split()[2][0]
		globals()['gadi_used_project'] = gadioutput[3].split()[1] + " " + gadioutput[3].split()[2][0]
		globals()['gadi_reserved_project'] = gadioutput[4].split()[1] + " " + gadioutput[4].split()[2][0]
		globals()['gadi_avail_project'] = gadioutput[5].split()[1] + " " + gadioutput[5].split()[2][0]
		for i in range(0, len(gadioutput) - 2):
			if globals()['gadiusername'] in gadioutput[i]:
				globals()['gadi_used_me'] = gadioutput[i].split()[1] + " " + gadioutput[i].split()[2][0]
				globals()['gadi_reserved_me'] = gadioutput[i].split()[3] + " " + gadioutput[i].split()[4][0]
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
	return(globals()['gadi_used_me'] + "/" + globals()['gadi_reserved_me'])


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

# for i in range(200):
# 	print(gadiusageproject())
# 	print(gadiusageme())
# 	print(gadihomequota())

# 	time.sleep(3)

