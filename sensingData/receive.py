import os

class Receive:
	def __init__(self, sensorControl, cameraIpPort, topic):
		self.sensorControl = sensorControl
		self.cameraIpPort = cameraIpPort
		self.topic = topic

	def getData(self, raspid):
		if self.topic.flag == True:
			print("take Topic")
			self.topic.flag = False

			if raspid == self.topic.topic[0:len(raspid)] :
				topic = self.topic.topic[len(raspid) + 1:]
			else :
				topic = ""

			for i, sender in enumerate(self.topic.TakeTopic):
				if topic == sender:
					senderData = self.matchingTopic(i)
					self.sender(senderData)
					break

	def matchingTopic(self, messgeSenderindex):
		print("start matching Topic")
		data = self.topic.data
		for messageNum, message in enumerate(self.topic.MessageList[messgeSenderindex]):
			if data == message :
				return [messgeSenderindex, messageNum]
			
		return [messgeSenderindex, ""]

	def sender(self, senderData):
		print("sender Topic")
		if senderData[0] == 0 :
			self.senderIsCom(senderData[1])
		elif senderData[0] == 1:
			self.senderIsPhone(senderData[1])
		elif senderData[0] == 2:
			self.senderIsDServer(senderData[1])
		elif senderData[0] == 3:
   			self.senderIsMove(senderData[1])	

	def senderIsCom(self, senderMesaage):
		print("sender is com")
		if senderMesaage == 0:
			for i, sensorTimerControl in enumerate(self.sensorControl[0]):
				sensorTimerControl.getNowData()
			
			for i, sensorDetectControl in enumerate(self.sensorControl[1]):
				sensorDetectControl.getNowData()

			for i, cameraIpPortInfo in enumerate(self.cameraIpPort):
				self.topic.setSendMessageTopic(2, i,cameraIpPortInfo)

		elif senderMesaage == 1:
			for i, sensorTimerControl in enumerate(self.sensorControl[0]):
				sensorTimerControl.getNowData()
			
			for i, sensorDetectControl in enumerate(self.sensorControl[1]):
				sensorDetectControl.getNowData()
			
		elif senderMesaage == 2:
			for i, cameraIpPortInfo in enumerate(self.cameraIpPort):
				self.topic.setSendMessageTopic(2, i, cameraIpPortInfo)

		elif senderMesaage == 3:
			for i, sensorDetectControl in enumerate(self.sensorControl[1]):
				sensorDetectControl.lastdataClear()
				self.topic.setSendMessageTopic(1, i, sensorDetectControl.detectCheck)
			return True
		
		elif senderMesaage == 4:
			os.popen('sudo reboot').read()

	def senderIsPhone(self, senderMesaage):
		print("sender is phone")
		if senderMesaage == 0:
			for i, sensorTimerControl in enumerate(self.sensorControl[0]):
				sensorTimerControl.getNowData()
			
			for i, sensorDetectControl in enumerate(self.sensorControl[1]):
				sensorDetectControl.getNowData()

			for i, cameraIpPortInfo in enumerate(self.cameraIpPort):
				self.topic.setSendMessageTopic(2, i, cameraIpPortInfo)

		elif senderMesaage == 1:
			for i, sensorTimerControl in enumerate(self.sensorControl[0]):
				sensorTimerControl.getNowData()
			
			for i, sensorDetectControl in enumerate(self.sensorControl[1]):
				sensorDetectControl.getNowData()
			
		elif senderMesaage == 2:
			for i, cameraIpPortInfo in enumerate(self.cameraIpPort):
				self.topic.setSendMessageTopic(2, i, cameraIpPortInfo)

		elif senderMesaage == 3:
			for i, sensorDetectControl in enumerate(self.sensorControl[1]):
				sensorDetectControl.lastdataClear()
				self.topic.setSendMessageTopic(1, i, sensorDetectControl.detectCheck)
			return True
			
		elif senderMesaage == 4:
			os.popen('sudo reboot').read()	

	def senderIsDServer(self, senderMesaage):
		print("sender is DServer")			
		if senderMesaage == 0:
			for i, cameraIpPortInfo in enumerate(self.cameraIpPort):
 				self.topic.setSendMessageTopic(2, i, cameraIpPortInfo)
		elif senderMesaage == 1:
			for i, cameraIpPortInfo in enumerate(self.cameraIpPort):
				self.topic.setSendMessageTopic(2, i, cameraIpPortInfo)
		
	def senderIsMove(self, senderMesaage):
		print("sender send to Move")
		if self.sensorControl[2] != []:
			self.sensorControl[2][0].write(senderMesaage)