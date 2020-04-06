import RPi.GPIO as GPIO
import time
import sensor
import os

# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

localIp = os.popen('hostname -I').read() ##  local ip
localPort = "8891"

localGlobalIp = os.popen('curl ifconfig.me').read() ## global ip
cameraPort = "11092"

if localIp == localGlobalIp:
	cameraIpPort =[localGlobalIp, localPort]
else :
	cameraIpPort = [localGlobalIp , cameraPort]

# dev server IP
brokerIpPort = ["124.139.136.86", "1883"]

cameraCheck = os.system('sh /home/pi/raspstart/mjpg.sh &') ##

# Can Use GPIO
mainInstance = sensor.Sensor(GPIO, brokerIpPort, cameraIpPort)

def startToSensing():
	mainInstance.sensingStart()

try:
	print("start")
	while True:
		startToSensing()

except KeyboardInterrupt:
	GPIO.cleanup()
