class LED:
	def __init__(self, pin_R, pin_G, GPIO):
		self.GPIO = GPIO
		self.__pin_R = pin_R
		self.__pin_G = pin_G
		self.setting()

	def setting(self):
		self.GPIO.setup(self.__pin_G, self.GPIO.OUT)
		self.GPIO.setup(self.__pin_R, self.GPIO.OUT)

	def write(self, i):
		if(i == 0):
			self.GPIO.output(self.__pin_G, False)
			self.GPIO.output(self.__pin_R, True)
		elif(i == 1):
			self.GPIO.output(self.__pin_G, True)
			self.GPIO.output(self.__pin_R, False)
