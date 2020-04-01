import Connect

class SendTopic :
    sendTopic = ["tcs/temp", "tcs/humid",  "tcs/fire", "tcs/shock", "tcs/ir", "tcs/clear", "tcs/localip", "test/broker"]
    getTopic = ["tcs/com", "test/phone"]

    flag = ""

    def __init__(self, ipPort):
        self.connect = Connect.Connect(ipPort)
        self.initToSub()

    def getFlag(self):
	    return self.flag

    def setFlag(self, data):
        self.flag = data

    def send(self, sensorNum, data):
        self.connect.sendPublish(self.sendTopic[sensorNum], data)


    def initToSub(self):
    	print("MQTT-initTosub")

	def on_connect(client, userdata, flags, rc):
		print("MQTT-onConnect - " + str(rc))
		for i in self.getTopic :
			self.connect.setSubscribe(i)

        def on_message(client, userdata, msg):
    		print("MQTT-onMessage")
	    	self.flag = str(msg.payload)

	self.connect.setOnConnect(on_connect)
	self.connect.setOnMessage(on_message)
