import RPi.GPIO as GPIO
import sensor
import os

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

localGlobalIp = os.popen('curl ifconfig.me').read()
# localIp = os.popen('hostname -I').read() 

cameraCheck = os.system('sh /home/pi/raspstart/mjpg.sh &')

ipPort = ["124.139.136.86", "1883"]

cameraPort = "8891"




mainInstance = sensor.Sensor(GPIO, localGlobalIp, ipPort, cameraPort)

def startToSensing():
		mainInstance.sensing()

try:
	print("start")
	while True:
		startToSensing()

except KeyboardInterrupt:
	GPIO.cleanup()
