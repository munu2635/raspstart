import datetime
import time
import Topic
import receive

import DHT11
import PM2008M
import Shock
import Fire
import Cds 
import IR

import Gas
import Button
import LED
import SG90

class Sensing :

	def __init__(self, GPIO, allIpPort, raspid, sensordata):
		self.tHCount = 0
		self.GPIO = GPIO
		self.brokerIpPort = allIpPort[0]
		self.cameraIpPort = allIpPort[1]

		self.all_pin = sensordata[0]
		self.adc_pin = sensordata[1]
		self.useSensor = sensordata[2]
		self.ButtonUpDown = sensordata[3]

		self.topic = Topic.Topic(self.brokerIpPort, raspid)
		self.raspid = raspid

		self.reciveControl = False
		self.sensorTimerControl = []
		self.sensorDetectControl = []
		
		self.sensorTimerControlIndex = []
		self.sensorDetectControlIndex = []

		self.sensorMoveControl = []


		self.setInstance(GPIO)
		self.receive = receive.Receive([self.sensorTimerControl, self.sensorDetectControl, self.sensorMoveControl], self.cameraIpPort, self.topic)

	def setInstance(self, GPIO):
		if self.useSensor[0] :
			self.sensorTimerControl.append(DHT11.Control(self.all_pin[0], GPIO, self.topic,[0, 1]))
			self.sensorTimerControlIndex.append(0)
			self.sensorTimerControlIndex.append(1)
		if self.useSensor[1] :
			self.sensorDetectControl.append(Fire.Control(self.all_pin[1], GPIO, self.topic, 0))
			self.sensorDetectControlIndex.append(0)
		if self.useSensor[2] :
			self.sensorDetectControl.append(Shock.Control(self.all_pin[4], GPIO, self.topic, 1))
			self.sensorDetectControlIndex.append(1)
		if self.useSensor[3] :
			self.sensorDetectControl.append(IR.Control(self.all_pin[5], GPIO, self.topic, 2))
			self.sensorDetectControlIndex.append(2)
		if self.useSensor[4] :
			self.sensorDetectControl.append(Gas.Control(self.adc_pin[0], self.topic, 3))
			self.sensorDetectControlIndex.append(3)
		if self.useSensor[5] :
			self.sensorTimerControl.append(Cds.Control(self.all_pin[7], GPIO, self.topic, 2))
			self.sensorTimerControlIndex.append(2)
		if self.useSensor[6] :
			self.button_instance = Button.Control(self.all_pin[6], GPIO, self.topic)
		if self.useSensor[7] :
			self.led_instance = LED.LED(self.all_pin[2], self.all_pin[3], GPIO)
			self.led_instance.write(1)
		if self.useSensor[8] :
			self.sensorMoveControl.append(SG90.SG90(self.all_pin[8], self.all_pin[9], GPIO))
		if self.useSensor[9] :
    		self.sensorTimerControl.append(PM2008M.Control(self.topic,[3, 4]))
			self.sensorTimerControlIndex.append(3)
			self.sensorTimerControlIndex.append(4)
	

	def sensingStart(self):
		self.sensingList()
		self.reciveControl = self.receive.getData(self.raspid)

	def sensingList(self):
		try:
			for i in self.sensorTimerControl :
				i.check()
	
			for i in self.sensorDetectControl :
				data = i.check()
				if data == 1 and self.useSensor[7] :
					self.led_instance.write(0)
	
			if self.useSensor[6] :
				if self.ButtonUpDown : 
					if self.button_instance.clearButtonUp(self.sensorDetectControl, self.sensorDetectControlIndex):
						self.led_instance.write(1)
				else :
					if self.button_instance.clearButtonDown(self.sensorDetectControl, self.sensorDetectControlIndex ):
						self.led_instance.write(1)
			
			if self.reciveControl :
				self.reciveControl = False 
				self.led_instance.write(1)
				
		except KeyboardInterrupt:
			self.GPIO.cleanup()