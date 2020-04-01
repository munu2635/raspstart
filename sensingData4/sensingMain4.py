import RPi.GPIO as GPIO
import sensor
import os

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

localIp = os.popen('hostname -I').read() 

cameraCheck = os.system('home/pi/raspstart/mjpg.sh')

mainInstance = sensor.Sensor(GPIO, localIP)

def startToSensing():
		mainInstance.sensing()

try:
	print("start")
	while True:
		startToSensing()

except KeyboardInterrupt:
	GPIO.cleanup()
