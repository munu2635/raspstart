import sensorGpio
import datetime
import Topic

class Sensor :
	all_pin = [22, 25, 24, 23, 27, 16, 26]
	# dht11_pin = 22 / fire_pin = 25 / led_red_pin = 24 / led_green_pin = 23
	# shock_pin = 27 / ir_sensor_pin = 16 / button_pin = 26W

	lastdata = ["0", "0", "0", "0", "0", "0"]

	def __init__(self, GPIO, brokerIpPort, cameraIpPort):
		self.tHCount = 0
		self.brokerIpPort = brokerIpPort
		self.cameraIpPort = cameraIpPort
		self.topic = Topic.SendTopic(brokerIpPort)

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
		self.tempHumidCheck()
		self.fireCheck()
		self.irCheck()
		self.shockCheck()
		self.clearButton()
		self.getData()

	def getData(self):
		if self.topic.flag == True:
			topic = self.topic.topic
			for i, sender in enumerate(self.topic.TakeTopic):
				if topic == sender:
					senderData = self.matchingTopic(i)
					sender = [senderData]

	def matchingTopic(self, messgeSenderindex):
		data = self.topic.data
		for Listnum, messageList in enumerate(self.topic.MessgeList[messgeSenderindex]):
			for messageNum, message in enumerate(messageList):
				if data == message :
					self.topic.flag = False
					return [Listnum, messageNum]

	def sender(self, senderData):
		if senderData[0] == 0 :
			senderIsCom(senderData[1])
		elif senderData[0] == 1:
			senderIsPhone(senderData[1])
		elif senderData[0] == 2:
			senderIsDServer(senderData[1])	

	def senderIsCom(self, senderMesaage):
		print("com")

	# phoneMessage = ["start", "get", "IpPort"]
	def senderIsPhone(self, senderMesaage):
		if senderMesaage == 0:
			for i, lastadata in enumerate(lastdata):
				self.topic.setSenderMesaageTopic(i, lastadata)
			
			self.topic.setSenderMesaageTopic(6, self.cameraIpPort[0])
			self.topic.setSenderMesaageTopic(7, self.cameraIpPort[1])
			self.topic.setSenderMesaageTopic(8, "send-start")
		elif senderMesaage == 1:
			for i, lastadata in enumerate(lastdata):
				self.topic.setSenderMesaageTopic(i, lastadata)
			self.topic.setSenderMesaageTopic(8, "send-get")
		elif senderMesaage == 2:
			self.topic.setSenderMesaageTopic(6, self.cameraIpPort[0])
			self.topic.setSenderMesaageTopic(7, self.cameraIpPort[1])

	# detectServerMessage = ["start", "IpPort", "true", "dStart", "dEnd"] 
	def senderIsDServer(self, senderMesaage):
		if senderMesaage == 0:	
			self.topic.setSenderMesaageTopic(6, self.cameraIpPort[0])
			self.topic.setSenderMesaageTopic(7, self.cameraIpPort[1])
			self.topic.setSenderMesaageTopic(8, "send-start")
		elif senderMesaage == 1:
			self.topic.setSenderMesaageTopic(6, self.cameraIpPort[0])
			self.topic.setSenderMesaageTopic(7, self.cameraIpPort[1])

	def tempHumidCheck(self): # 0, 1
		result = self.dht11_instance.read()
		if result.is_valid():

			now_time = "Last valid input: " + str(datetime.datetime.now())
			temp = "Temperature: %d C" % result.temperature
			humid = "Humidity: %d %%" % result.humidity
			
			self.lastdata[0] = temp
			self.lastdata[1] = humid

			if(self.tHCount == 5):
				self.topic.setSenderMesaageTopic(0, temp)
				self.topic.setSenderMesaageTopic(1, humid)
				self.tHCount = 0

				print(now_time)
				print("MQTT-send - " + temp)
				print("MQTT-send - " + humid)


			self.tHCount += 1

	def fireCheck(self): # 2 
		read = self.instance[2].read()
		if read == 1:
			self.topic.setSenderMesaageTopic(2, 1)
			self.lastdata[2] = "1"
			self.instance[2].write(0)
			print(datetime.datetime.now())
			print("MQTT-send -" + "fire")

	def shockCheck(self): # 3
		read = self.instance[3].read()
		if read == 1:
			self.topic.setSenderMesaageTopic(3, 1)
			self.lastdata[3] = "1"
			self.instance[3].write(0)
			print(str(datetime.datetime.now()))
			print("MQTT-send - " + "shock")

	def irCheck(self): # 4
		read = self.instance[4].read()
		if read == 0:
			self.topic.setSenderMesaageTopic(4, 1)
			self.lastdata[4] ="1"
			self.instance[4].write(0)
			print(str(datetime.datetime.now()))
			print("MQTT-send - " + "detect")

	def clearButton(self): # 5
		read = self.instance[5].read()

		if read == 0 :
			for i in range(3, 7):
				if i == 6:
					self.topic.setSenderMesaageTopic(i, 1)
				else :
					self.lastdata[i] = "0"
					self.topic.setSenderMesaageTopic(i, 0)

			print(str(datetime.datetime.now()))
			print("MQTT-send - clear")
			self.led_instance.write(1)
