import sensorGpio
import datetime
import mqtt

class Sensor :
	all_pin = [22, 25, 24, 23, 27, 16, 26]
	# dht11_pin = 22 / fire_pin = 25 / led_red_pin = 24 / led_green_pin = 23
	# shock_pin = 27 / ir_sensor_pin = 16 / button_pin = 26
	getflag = ""

	sending = mqtt.Connect("localhost", getflag)

	def __init__(self, GPIO):
		self.tHCount = 0 

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

	def getData(self):
		if self.getflag == "start" :
			self.sendAll()

	def sendAll(self):
			self.sending.send("temp", self.dht11_instance.lastTemp)
			self.sending.send("humid", self.dht11_instance.lastHumid)
			self.sending.send("fire", self.fire_instance.lastFire)
			self.sending.send("shock", self.shock_instance.lastShock)
			self.sending.send("ir", self.ir_instance.lastIR)

	def tempHumidCheck(self):
		result = self.dht11_instance.read()
		if result.is_valid():

			now_time = "Last valid input: " + str(datetime.datetime.now())
			temp = "Temperature: %d C" % result.temperature
			humid = "Humidity: %d %%" % result.humidity
			
			self.dht11_instance.lastHumid = temp
			self.dht11_instance.lastTemp = humid

			if(self.tHCount == 5):
				self.sending.send("temp", temp)
				self.sending.send("humid", humid)
				self.tHCount = 0

				print(now_time)
				print("MQTT-send - " + temp)
				print("MQTT-send - " + humid)


			self.tHCount += 1

	def fireCheck(self):
		read = self.fire_instance.read()
		if read == 1:
			self.sending.send("fire", 1)
			self.fire_instance.lastFire = "1"
			self.led_instance.write(0)
			print(datetime.datetime.now())
			print("MQTT-send -" + "fire")

	def shockCheck(self):
		read = self.shock_instance.read()
		if read == 1:
			self.sending.send("shock", 1)
			self.ir_instance.lastShock = "1"
			self.led_instance.write(0)
			print(str(datetime.datetime.now()))
			print("MQTT-send - " + "shock")

	def irCheck(self):
		read = self.ir_instance.read()
		if read == 0:
			self.sending.send("ir", 1)
			self.ir_instance.lastIR ="1"
			self.led_instance.write(0)
			print(str(datetime.datetime.now()))
			print("MQTT-send - " + "detect")

	def clearButton(self):
		read = self.clear_instance.read()

		if read == 0 :
			self.sending.send("fire", 0)
			self.sending.send("shock", 0)
			self.sending.send("ir", 0)
			self.sending.send("clear", 1)
			print(str(datetime.datetime.now()))
			print("MQTT-send - clear")
			self.led_instance.write(1)

			self.fire_instance.lastFire = "0"
			self.shock_instance.lastShock = "0"
			self.ir_instance.lastIR ="0"
