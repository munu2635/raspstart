import paho.mqtt.client as mqtt

class Connect :
    sendTopic = ["tcs/temp", "tcs/humid",  "tcs/fire", "tcs/shock", "tcs/ir", "tcs/clear"]
	# topic_temp = "tcs/temp" // topic_humid = "tcs/humid" // topic_fire = "tcs/fire"
	# topic_shock = "tcs/shock" // topic_IR = "tcs/ir" // topic_clear = "tcs/clear"
    getTopic = ["tcs/com", "tcs/phone"]
    msgList = ["start", "get"]

    client = mqtt.Client()

    def __init__(self, conIp, flag):
        print("MQTT-init")
        self.initToSub()
        self.client.connect("localhost")
        print("MQTT-connrct")
        self.flag = flag

        try:
            self.client.loop_start()
        except KeyboardInterrupt:
            print("Finished-connect")
            self.client.unsubscribe(self.getTopic)
            self.client.loop_stop()
            self.client.disconnect()

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

        self.client.publish(self.sendTopic[num], data)

    def initToSub(self):
        print("MQTT-initTosub")
        #def on_connect(client, userdata, rc):
        #   print("connected with result code " + str(rc))
        print("MQTT-onConnect")
        for i in self.getTopic :
            self.client.subscribe(i)

        def on_message(client, userdata, msg):
            print("Topic: " + msg.topic + " Message: " + str(msg.payload))
            print("MQTT-onMessage")

            if msg.topic == self.getTopic[1]:
                if str(msg.payload) == self.msgList[0]:
                    self.flag = self.msgList[0]
                elif str(msg.payload) == self.msgList[1]:
                    self.flag = self.msgList[1]

#        self.client.on_connect = on_connect
        self.client.on_message = on_message

