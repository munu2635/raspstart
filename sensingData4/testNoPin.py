import sensorGpio
import datetime
import sensorTopic

class Sensor :
	all_pin = [22, 25, 24, 23, 27, 16, 26]
	# dht11_pin = 22 / fire_pin = 25 / led_red_pin = 24 / led_green_pin = 23
	# shock_pin = 27 / ir_sensor_pin = 16 / button_pin = 26

	def __init__(self, GPIO, localIP, ipPort, cameraPort):
		self.localIp = localIP
		self.ipPort = ipPort
		self.cameraPort = cameraPort
		self.sending = sensorTopic.SendTopic(ipPort)


	def sensing(self):
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
