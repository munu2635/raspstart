import paho.mqtt.client as mqtt

class Connect :

    client = mqtt.Client()

    def __init__(self, ipPort):
	print("MQTT-init")
	self.client.connect(ipPort[0], ipPort[1])
        print("MQTT-connect")

        try:
		    self.client.loop_start()
        except KeyboardInterrupt:
		    print("Finished-connect")
		    self.client.unsubscribe(self.getTopic)
		    self.client.loop_stop()
		    self.client.disconnect()

    def sendPublish(self, Topic, data):
        self.client.publish(Topic, data)

    def setSubscribe(self, i):
        self.client.subscribe(i)

    def setOnConnect(self, on_connect):
        self.client.on_connect = on_connect

    def setOnMessage(self, on_message):
        self.client.on_message = on_message
