
# raspid + "/" + Topic
# topic - id/sendTopic

sensorTimerTopic = ["tcs/rasp/temp", "tcs/rasp/humid", "tcs/rasp/cds"]
sensorDetectTopic = ["tcs/rasp/fire", "tcs/rasp/shock", "tcs/rasp/ir", "tcs/rasp/gas", "tcs/rasp/cds"]

IpPortTopic = ["tcs/rasp/localIp", "tcs/rasp/cameraPort", "tcs/rasp/localIpUnder"]

sendTopic = [sensorTimerTopic, sensorDetectTopic, IpPortTopic]


TakeTopic = ["tcs/com", "tcs/phone", "tcs/detectServer", "tcs/rasp/move"]

computerMessage = ["start", "get", "ipPort", "ok", "reboot"]
phoneMessage = ["start", "get", "ipPort", "ok", "reboot"]
detectServerMessage = ["start", "ipPort", "true", "dStart", "dEnd"]
moveMessage = ["plus", "minus", "up", "down"]

MessageList = [computerMessage, phoneMessage, detectServerMessage, moveMessage]