import ASUS.GPIO as GPIO
import os
import time
import datetime
import subprocess
from auxiliary import parser
from auxiliary import defaults

fan = False
ttsleep = 10
gpiopin = 40
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(gpiopin, GPIO.OUT)
GPIO.output(gpiopin, 0)

pairs = parser.getparametersandvals(parser.getvalfromconfigbykeyword(defaults.config,defaults.keywords,defaults.configuration,[""]), defaults.parameters, "=", [" ", "	"], ",")
hot = float(parser.extractvaluebyparam(defaults.Temp_max_th, pairs)[0])
dtp = float(parser.extractvaluebyparam(defaults.Temp_step, pairs)[0])
logfile = parser.extractvaluebyparam(defaults.LogFile, pairs)[0]
lastev = parser.extractvaluebyparam(defaults.LastActionFile, pairs)[0]

def gettemp():
	temp_t = subprocess.check_output(['cat', '/sys/class/thermal/thermal_zone1/temp']).decode("utf-8")
	temp = temp_t[:-4] + '.' + temp_t[2:]
	return float(temp)

	
def filllogfile(logfile, lastev, fan, now):
	strstat = ""
	strstat = now.strftime("%d.%m.%Y %H:%M") + " [Fan status: " + str(fan) + "]\n"

	f = open(logfile, 'a')        
	f.write(strstat)
	f.close()
        
	f = open(lastev, 'w')
	f.write(strstat)
	f.close()
	
while True:
	time.sleep(ttsleep)
	temp = gettemp()
	now = datetime.datetime.now()
	
	if temp >= hot and fan == False:
		GPIO.output(gpiopin, 1)
		fan = True
		filllogfile(logfile + now.strftime("_%d.%m.txt"), lastev + now.strftime("%d-%m.txt"), fan, now)
	
	if (temp < hot - dtp) and fan == True:
		GPIO.output(gpiopin, 0)
		fan = False
		filllogfile(logfile + now.strftime("_%d.%m.txt"), lastev + now.strftime("%d-%m.txt"), fan, now)