import smbus
import datetime

class PM2008M :
    i2c = smbus.SMBus(1)
    loc = 0x28
    TxBuffer = [0x16, 0x7, 0x3, 0xFF, 0xFF, 0, 0x16] 

    def read(self) :
        self.i2c.write_i2c_block_data(self.loc, 0x50, self.TxBuffer) 
        value_buffer = self.i2c.read_i2c_block_data(self.loc, 0x51)
        
        if value_buffer[1] == 32 and value_buffer[0] == 0x16 :
            self.pm2p5_grimm = (value_buffer[9] << 8) + value_buffer[10]
            self.pm10_grimm = (value_buffer[11] << 8) + value_buffer[12]
            self.pm2p5_tsi = (value_buffer[15] << 8) + value_buffer[16]
            self.pm10_tsi = (value_buffer[17] << 8) + value_buffer[18]
            return [self.pm2p5_grimm, self.pm10_grimm]
        
        return [0, 0]

    def getPm2p5Grimm(self):
        return self.pm2p5_grimm

    def getPm10Grimm(self):
        return self.pm10_grimm

    def getPm2p5Tsi(self):
        return self.pm2p5_tsi
    
    def getPm105Tsi(self):
        return self.pm10_tsi


class Control:
    def __init__(self, topic, topicNum):
        self.pm2008m_instance = PM2008M()
        self.topic = topic
        self.pm10TopicNum = topicNum[0]
        self.pm2p5TopicNum = topicNum[1]
        self.detectCheckLastTime = ""
        self.lastdata = ["", ""]
        self.tHCount = 0
        
    def check(self):
        result = self.pm2008m_instance.read()
        pm2p5 = result[0]
        pm10 = result[1]

        self.lastdata[0] = pm10
        self.lastdata[1] = pm2p5

        if(self.tHCount == 20):
            self.topic.setSendMessageTopic(0, self.pm10TopicNum, pm10)
            self.topic.setSendMessageTopic(0, self.pm2p5TopicNum, pm2p5)
            self.tHCount = 0
            print("MQTT-send - %f" % (pm2p5))
            print("MQTT-send - %f" % (pm10))
        
        self.tHCount += 1

	def getNowData(self):
		self.topic.setSendMessageTopic(0, self.tempTopicNum, self.lastdata[0])
		self.topic.setSendMessageTopic(0, self.humidTopicNum, self.lastdata[1])