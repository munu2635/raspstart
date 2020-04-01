import sensorGpio
import datetime
import sensorTopic

class Sensor :
	all_pin = [22, 25, 24, 23, 27, 16, 26]

	def __init__(self, GPIO, localIP, ipPort, cameraPort):
		self.tHCount = 0
		self.localIp = localIP
		self.ipPort = ipPort
		self.cameraPort = cameraPort
		self.sending = sensorTopic.SendTopic(ipPort)


		self.dht11_instance = sensorGpio.DHT11(pin = self.all_pin[0], GPIO = GPIO)
		self.fire_instance = sensorGpio.Fire(pin = self.all_pin[1], GPIO = GPIO)
		self.shock_instance = sensorGpio.Shock(pin = self.all_pin[4], GPIO = GPIO)
		self.ir_instance = sensorGpio.IR(pin = self.all_pin[5], GPIO = GPIO)
		self.led_instance = sensorGpio.LED(pin_G = self.all_pin[3], pin_R = self.all_pin[2], GPIO = GPIO)
		self.clear_instance = sensorGpio.Button(pin = self.all_pin[6], GPIO = GPIO)

		self.led_instance.write(1)

	def sensing(self):
		self.tempHumidCheck()
		self.fireCheck()
		self.irCheck()
		self.shockCheck()
		self.clearButton()
		self.getData()

	def getData(self):
		if self.sending.getFlag() == "start" :
			self.sendAll(0)
			self.sending.setFlag(".")
		elif self.sending.getFlag() == "get" :
			self.sendAll(1)
			self.sending.setFlag(".")
		elif self.sending.getFlag() == "localIP" :
			self.sendAll(2)
			self.sending.setFlag(".")

	def sendAll(self, i):
		if i == 0 :
			self.sending.send(0, 0)
			self.sending.send(1, 0)
			self.sending.send(2, 0)
			self.sending.send(3, 0)
			self.sending.send(4, 0)
			self.sending.send(6, self.localIp)
			self.sending.send(7, self.cameraPort)
			self.sending.send(8, "send-start")
		elif i == 1:
			self.sending.send(0, 1)
			self.sending.send(1, 2)
			self.sending.send(2, 3)
			self.sending.send(3, 4)
			self.sending.send(4, 5)
			self.sending.send(6, self.localIp)	
			self.sending.send(7, self.cameraPort)	
			self.sending.send(8, "send-start")
		elif i == 2:
			self.sending.send(6, self.localIp)
			self.sending.send(7, self.cameraPort)	

	def tempHumidCheck(self):
		result = self.dht11_instance.read()
		if result.is_valid():

			now_time = "Last valid input: " + str(datetime.datetime.now())
			temp = "Temperature: %d C" % result.temperature
			humid = "Humidity: %d %%" % result.humidity
			
			self.dht11_instance.lastHumid = temp
			self.dht11_instance.lastTemp = humid

			if(self.tHCount == 5):
				self.sending.send(0, temp)
				self.sending.send(1, humid)
				self.tHCount = 0

				print(now_time)
				print("MQTT-send - " + temp)
				print("MQTT-send - " + humid)


			self.tHCount += 1

	def fireCheck(self):
		read = self.fire_instance.read()
		if read == 1:
			self.sending.send(2, 1)
			self.fire_instance.lastFire = "1"
			self.led_instance.write(0)
			print(datetime.datetime.now())
			print("MQTT-send -" + "fire")

	def shockCheck(self):
		read = self.shock_instance.read()
		if read == 1:
			self.sending.send(3, 1)
			self.ir_instance.lastShock = "1"
			self.led_instance.write(0)
			print(str(datetime.datetime.now()))
			print("MQTT-send - " + "shock")

	def irCheck(self):
		read = self.ir_instance.read()
		if read == 0:
			self.sending.send(4, 1)
			self.ir_instance.lastIR ="1"
			self.led_instance.write(0)
			print(str(datetime.datetime.now()))
			print("MQTT-send - " + "detect")

	def clearButton(self):
		read = self.clear_instance.read()

		if read == 0 :
			self.sending.send(3, 0)
			self.sending.send(4, 0)
			self.sending.send(5, 0)
			self.sending.send(6, 1)
			print(str(datetime.datetime.now()))
			print("MQTT-send - clear")
			self.led_instance.write(1)

			self.fire_instance.lastFire = "0"
			self.shock_instance.lastShock = "0"
			self.ir_instance.lastIR ="0"
