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
		self.lastdata = 0

	def check(self):
		read = self.cds_instance.read()
		
		if read == False and self.lastdata == 0 :  
			self.lastdata = 1 # on
			self.topic.setSendMessageTopic(0, self.topicNum, self.lastdata)
			print("MQTT-send - " + "cds")

			return False
		elif read == True and self.lastdata == 1 :
			self.lastdata = 0 # off
			self.topic.setSendMessageTopic(0, self.topicNum, self.lastdata)

			print("MQTT-send - " + "cds")
			return True

	def getNowData(self):
			self.topic.setSendMessageTopic(0, self.topicNum, self.lastdata)