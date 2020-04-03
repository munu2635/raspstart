import Connect

class Topic :

    sendTopic = ["tcs/rasp1/temp", "tcs/rasp1/humid",  "tcs/rasp1/fire", "tcs/rasp1/shock", 
    "tcs/rasp/ir", "tcs/rasp/clear", "tcs/rasp/localIp", "tcs/rasp/cameraPort",
     "test/rasp/broker"]

    TakeTopic = ["tcs/com", "tcs/phone", "tcs/detectServer"]

    computerMessage = ["", ""]
    phoneMessage = ["start", "get", "ipPort"]
    detectServerMessage = ["start", "ipPort", "true", "dStart", "dEnd"]

    MessageList = [computerMessage, phoneMessage, detectServerMessage]
    
    raspdata = ["id", sendTopic, MessageList, TakeTopic] 

    # topic - id/sendTopic 


    flag = False
    topic = ""
    data = ""

    def __init__(self, ipPort):
        self.connect = Connect.Connect(ipPort)
        self.initToSub()

    def setTakeMassageTopic(self, topic):
        self.connect.setSubscribe(topic)

    def setSendMessageTopic(self, sensorNum, data):
        self.connect.setPublish(self.sendTopic[sensorNum], data)

    def initToSub(self):
        print("MQTT-initTosub")
        def on_connect(client, userdata, flags, rc):
            print("MQTT-onConnect - " + str(rc))
            for i in self.TakeTopic :
                self.setTakeMassageTopic(i)

        def on_message(client, userdata, msg):
            print("MQTT-onMessage")
            self.flag = True
            self.topic = str(msg.topic)
            self.data = str(msg.payload)

        self.connect.setOnConnect(on_connect)
        self.connect.setOnMessage(on_message)
