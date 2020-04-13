import datetime
# timer

class Cds:
	def __init__(self, pin, GPIO):
		self.__pin = pin
		self.GPIO = GPIO
		self.setting()

	def setting(self):
		self.GPIO.setup(self.__pin, self.GPIO.IN)

	def read(self):
		return self.GPIO.input(self.__pin)

class Control:
	def __init__(self, pin, GPIO, topic, topicNum):
		self.cds_instance = Cds(pin, GPIO)
		self.topic = topic
		self.topicNum = topicNum

		self.detectCheckLastTime = ""
		self.lastdata = self.false

	def check(self):
		read = self.cds_instance.read()
		if read == self.false and self.lastdata == self.false :  
			self.lastdata = self.true
			self.topic.setSendMessageTopic(0, self.topicNum, self.lastdata)

			print("MQTT-send - " + "cds")
		elif read == self.false and self.lastdata == self.false :
			self.lastdata = self.false
			self.topic.setSendMessageTopic(0, self.topicNum, self.lastdata)

			print("MQTT-send - " + "cds")

	def getNowData(self):
			self.topic.setSendMessageTopic(0, self.topicNum, self.lastdata)