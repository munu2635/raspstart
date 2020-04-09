import sensorGpio
import datetime
import Topic

class Sensor :
	all_pin = [22, 25, 24, 23, 27, 16, 26, 6, 5]

	lastdatas = ["0", "0", "0", "0", "0", "0"]

	def __init__(self, GPIO,  allIpPort, raspid):
		self.tHCount = 0
		self.raspid = raspid
		self.brokerIpPort = allIpPort[0]
		self.cameraIpPort = allIpPort[1]
		self.topic = Topic.Topic(self.brokerIpPort, raspid)

		self.setInstance(GPIO)
		self.led_instance.write(1)

	def setInstance(self, GPIO):
		self.dht11_instance = sensorGpio.DHT11(pin = self.all_pin[0], GPIO = GPIO)
		self.fire_instance = sensorGpio.Fire(pin = self.all_pin[1], GPIO = GPIO)
		self.shock_instance = sensorGpio.Shock(pin = self.all_pin[4], GPIO = GPIO)
		self.ir_instance = sensorGpio.IR(pin = self.all_pin[5], GPIO = GPIO)
		self.led_instance = sensorGpio.LED(pin_G = self.all_pin[3], pin_R = self.all_pin[2], GPIO = GPIO)
		self.clear_instance = sensorGpio.Button(pin = self.all_pin[6], GPIO = GPIO)
		self.instance = [self.dht11_instance, self.fire_instance, self.shock_instance,
						self.ir_instance, self.led_instance, self.clear_instance]

	def sensingStart(self):
		self.sensingList()
		self.getData()

	def getData(self):
		if self.topic.flag == True:
			print("take Topic")
			self.topic.flag = False
			print(self.topic.topic[0:len(self.raspid)])

			if self.raspid == self.topic.topic[0:len(self.raspid)] :
				topic = self.topic.topic[len(self.raspid) + 1:]
			else :
				topic = ""

			for i, sender in enumerate(self.topic.TakeTopic):
				print(topic, i, sender)
				if topic == sender:
					senderData = self.matchingTopic(i)
					print(senderData)
					self.sender(senderData)
					break

	def matchingTopic(self, messgeSenderindex):
		print("start matching Topic")
		data = self.topic.data
		for messageNum, message in enumerate(self.topic.MessageList[messgeSenderindex]):
			print(data, messgeSenderindex, messageNum,  message)
			if data == message :
				return [messgeSenderindex, messageNum]

	def sender(self, senderData):
		print("sender Topic")
		if senderData[0] == 0 :
			self.senderIsCom(senderData[1])
		elif senderData[0] == 1:
			self.senderIsPhone(senderData[1])
		elif senderData[0] == 2:
			self.senderIsDServer(senderData[1])

	def senderIsCom(self, senderMesaage):
		print("sender is com")
		if senderMesaage == 0:
			for i, lastdata in enumerate(self.lastdatas):
				self.topic.setSendMessageTopic(i, lastdata)
			self.topic.setSendMessageTopic(6, self.cameraIpPort[0])
			self.topic.setSendMessageTopic(7, self.cameraIpPort[1])
		elif senderMesaage == 1:
			for i, lastdata in enumerate(self.lastdatas):
				self.topic.setSendMessageTopic(i, lastdata)
		elif senderMesaage == 2:
			self.topic.setSendMessageTopic(6, self.cameraIpPort[0])
			self.topic.setSendMessageTopic(7, self.cameraIpPort[1])

	def senderIsPhone(self, senderMesaage):
		print("sender is phone")
		if senderMesaage == 0:
			for i, lastdata in enumerate(self.lastdatas):
				self.topic.setSendMessageTopic(i, lastdata)
			self.topic.setSendMessageTopic(6, self.cameraIpPort[0])
			self.topic.setSendMessageTopic(7, self.cameraIpPort[1])
			self.topic.setSendMessageTopic(8, self.cameraIpPort[2])
		elif senderMesaage == 1:
			for i, lastdata in enumerate(self.lastdatas):
				self.topic.setSendMessageTopic(i, lastdata)
			self.topic.setSendMessageTopic(8, self.cameraIpPort[2])
		elif senderMesaage == 2:
			self.topic.setSendMessageTopic(6, self.cameraIpPort[0])
			self.topic.setSendMessageTopic(7, self.cameraIpPort[1])
			self.topic.setSendMessageTopic(8, self.cameraIpPort[2])

	def senderIsDServer(self, senderMesaage):
		print("sender is DServer")
		if senderMesaage == 0:
			self.topic.setSendMessageTopic(6, self.cameraIpPort[0])
			self.topic.setSendMessageTopic(7, self.cameraIpPort[1])
		elif senderMesaage == 1:
			self.topic.setSendMessageTopic(6, self.cameraIpPort[0])
			self.topic.setSendMessageTopic(7, self.cameraIpPort[1])

	def sensingList(self):
		self.tempHumidCheck()
		self.fireCheck()
		self.irCheck()
		self.shockCheck()
		self.clearButton()

	def tempHumidCheck(self):
		result = self.instance[0].read()
		if result.is_valid():

			now_time = "Last valid input: " + str(datetime.datetime.now())
			temp = "Temperature: %d C" % result.temperature
			humid = "Humidity: %d %%" % result.humidity

			self.lastdatas[0] = temp
			self.lastdatas[1] = humid

			if(self.tHCount == 5):
				self.topic.setSendMessageTopic(0, temp)
				self.topic.setSendMessageTopic(1, humid)
				self.tHCount = 0

				print(now_time)
				print("MQTT-send - " + temp)
				print("MQTT-send - " + humid)


			self.tHCount += 1

	def fireCheck(self):
		read = self.instance[1].read()
		if read == 0: #!! 1
			self.topic.setSendMessageTopic(2, 1)
			self.lastdatas[1] = "1"
			print(datetime.datetime.now())
			print("MQTT-send -" + "fire")

	def shockCheck(self):
		read = self.instance[2].read()
		if read == 0: #!! 1
			self.topic.setSendMessageTopic(3, 1)
			self.lastdatas[2] = "1"
			print(str(datetime.datetime.now()))
			print("MQTT-send - " + "shock")

	def irCheck(self):
		read = self.instance[3].read()
		if read == 0:
			self.topic.setSendMessageTopic(4, 1)
			self.lastdatas[3] ="1"
			print(str(datetime.datetime.now()))
			print("MQTT-send - " + "detect")

	def clearButton(self):
		read = self.instance[5].read()

		if read == 0:
			for i in range(2, 7):
				if i == 6:
					self.topic.setSendMessageTopic(i, 1)
				else :
					self.lastdatas[i] = "0"
					self.topic.setSendMessageTopic(i, 0)

			print(str(datetime.datetime.now()))
			print("MQTT-send - clear")
			self.led_instance.write(1)
