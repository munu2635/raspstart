import Connect
import settingTopic

class Topic :
    sendTopic = settingTopic.sendTopic
    TakeTopic = settingTopic.TakeTopic
    MessageList = settingTopic.MessageList

    flag = False
    topic = ""
    data = ""

    def __init__(self, ipPort, raspid):
        self.raspid = raspid
        self.connect = Connect.Connect(ipPort)
        self.initToSub()

    def setTakeMassageTopic(self, topic):
        self.connect.setSubscribe(self.raspid + "/"+ topic)

    def setSendMessageTopic(self, sensOrNot, num, data):
        self.connect.setPublish(self.raspid + "/" + self.sendTopic[sensOrNot][num], data)

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
