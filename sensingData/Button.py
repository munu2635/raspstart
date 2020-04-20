import datetime
# detect
class Button:
	def __init__(self, pin, GPIO):
		self.GPIO = GPIO
		self.__pin = pin
		self.setting()

	def setting(self):
		self.GPIO.setup(self.__pin, self.GPIO.IN)

	def read(self):
		return self.GPIO.input(self.__pin)

class Control:
	def __init__(self, pin, GPIO, topic):
		self.clear_instance = Button(pin, GPIO)
		self.topic = topic

	def clearButtonDown(self, sensorDetectControl):
		read = self.clear_instance.read()

		if read == 0:
			for i in range(0, len(sensorDetectControl)):
				sensorDetectControl[i].lastdataClear()
				self.topic.setSendMessageTopic(i, sensorDetectControl[i].detectCheck)

			print(str(datetime.datetime.now()))
			print("MQTT-send - clear")
			return True
	
	def clearButtonUp(self, sensorDetectControl):
		read = self.clear_instance.read()

		if read == 1:
			for i in range(0, len(sensorDetectControl)):
				sensorDetectControl[i].lastdataClear()
				self.topic.setSendMessageTopic(i, sensorDetectControl[i].detectCheck)

			print(str(datetime.datetime.now()))
			print("MQTT-send - clear")
			return True