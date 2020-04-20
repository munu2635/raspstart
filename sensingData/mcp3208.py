import spidev
import time

class MCP3208 :
    def __init__(self, usePin):
        self.spi = spidev.SpiDev()
        self.usePin = usePin
        self.spi.open(0, 1)
        self.spi.max_speed_hz = 1000000

    def analogRead(self):
        r = self.spi.xfer2([1, (8 + self.usePin) << 4, 0])
        adc_out = ((r[1]&3) << 8) + r[2]
        return adc_out

    def getVoltage(self, read) :
        return read * 3.3 / 1024