import paho.mqtt.client as mqtt

class Connect :

    client = mqtt.Client()
    topicList = list()

    def __init__(self, ipPort):
        print("MQTT-init")
        self.ipPort = ipPort
        print("MQTT-connect")

    def start(self):
        self.client.connect(self.ipPort[0], self.ipPort[1])
        try:
        	self.client.loop_start()
        except KeyboardInterrupt:
            print("Finished-connect")
            for i in self.topicList:
                self.client.unsubscribe(i)
            self.client.loop_stop()
            self.client.disconnect()


    def setPublish(self, Topic, data):
        self.client.publish(Topic, data, 0, False)

    def setSubscribe(self, i):
        self.client.subscribe(i)

    def setOnConnect(self, on_connect):
        self.client.on_connect = on_connect

    def setOnMessage(self, on_message):
        self.client.on_message = on_message
        
    def setWill(self, topic):
        self.client.will_set(topic, "off", qos=0, retain=False)