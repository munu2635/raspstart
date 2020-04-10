import RPi.GPIO as GPIO
import setting
import sensing
import os

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

cameraLocalIp = os.popen('hostname -I').read()
cameraGlobalIp = os.popen('curl ifconfig.me').read()

if cameraLocalIp == cameraGlobalIp:
	cameraIpPort = [cameraGlobalIp, setting.cameraGlobalport, cameraLocalIp]
else :
	cameraIpPort = [cameraGlobalIp, setting.cameraLocalport, cameraLocalIp]
	
#cameraCheck = os.system('sh /home/pi/raspstart/mjpg.sh &') ##

allIpPort = [setting.brokerIpPort, cameraIpPort]

mainInstance = sensing.Sensing(GPIO, allIpPort, setting.raspid, setting.sensordata)


def startToSensing():
		mainInstance.sensingStart()

try:
	print("start")
	while True:
		startToSensing()

except KeyboardInterrupt:
	GPIO.cleanup()
