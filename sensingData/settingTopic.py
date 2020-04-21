
# raspid + "/" + Topic
# topic - id/sendTopic

sensorTimerTopic = ["tcs/rasp/temp", "tcs/rasp/humid",  "tcs/rasp/cds", "tcs/rasp/pm2p5", "tcs/rasp/pm10"]
sensorDetectTopic = ["tcs/rasp/fire", "tcs/rasp/shock", "tcs/rasp/ir", "tcs/rasp/gas"]

ipPortTopic = ["tcs/rasp/localIp", "tcs/rasp/cameraPort", "tcs/rasp/localIpUnder"]

onOffTopic = ["tcs/rasp/onOff"]

sendTopic = [sensorTimerTopic, sensorDetectTopic, ipPortTopic, onOffTopic]

TakeTopic = ["tcs/com", "tcs/phone", "tcs/detectServer", "tcs/rasp/move"]

computerMessage = ["start", "get", "ipPort", "ok", "reboot"]
phoneMessage = ["start", "get", "ipPort", "ok", "reboot"]
detectServerMessage = ["start", "ipPort", "true", "dStart", "dEnd"]
moveMessage = ["plus", "minus", "up", "down"]

MessageList = [computerMessage, phoneMessage, detectServerMessage, moveMessage]