import paho.mqtt.client as mqtt

class Connect :
    sendTopic = ["tcs/temp", "tcs/humid",  "tcs/fire", "tcs/shock", "tcs/ir", "tcs/clear", "test/broker"]
	# topic_temp = "tcs/temp" // topic_humid = "tcs/humid" // topic_fire = "tcs/fire"
	# topic_shock = "tcs/shock" // topic_IR = "tcs/ir" // topic_clear = "tcs/clear"
    getTopic = ["tcs/com", "test/phone"]
    msgList = ["start", "get"]

    Topic = ""
    flag = ""

    client = mqtt.Client()

    def __init__(self, ipPort):
	    print("MQTT-init")
        self.initToSub()
        self.client.connect(ipPort[0], ipPort[1])
        print("MQTT-connect")


        try:
		self.client.loop_start()
        except KeyboardInterrupt:
		print("Finished-connect")
		self.client.unsubscribe(self.getTopic)
		self.client.loop_stop()
		self.client.disconnect()

    def getFlag(self):
	return self.flag

    def setFlag(self, data):
        self.flag = data

    def send(self, sensorName, data):

        num = 1
        if sensorName == "temp":
		num = 0
        elif sensorName == "humid":
		num = 1
        elif sensorName == "fire":
		num = 2
        elif sensorName == "shock":
		num = 3
        elif sensorName == "ir":
		num = 4
        elif sensorName == "clear":
		num = 5
        elif sensorName == "test":
		num = 6

        self.client.publish(self.sendTopic[num], data)

    def initToSub(self):
	print("MQTT-initTosub")

	def on_connect(client, userdata, flags, rc):
		print("connected result code " + str(rc))
		print("MQTT-onConnect")
		for i in self.getTopic :
			self.client.subscribe(i)

        def on_message(client, userdata, msg):
		print("Topic: " + msg.topic + " Message: " + str(msg.payload))
		print("MQTT-onMessage")
		self.flag = str(msg.payload)

	self.client.on_connect = on_connect
	self.client.on_message = on_message