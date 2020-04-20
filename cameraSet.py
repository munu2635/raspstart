import RPi.GPIO as GPIO
import os

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(4, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)


def main():
    GPIO.output(7, False)
    GPIO.output(11, False)
    GPIO.output(12, True)
    capture(1)

    GPIO.output(7, True)
    GPIO.output(11, False)
    GPIO.output(12, True)
    capture(2)

    GPIO.output(7, False)
    GPIO.output(11, True)
    GPIO.output(12, False)
    capture(3)

    GPIO.output(7, True)
    GPIO.output(11, True)
    GPIO.output(12, False)
    capture(4)

def capture(cam):
    cmd = "raspistill -o capture_%d.jpg" % cam
    os.system(cmd)

if __name__ == "__main__":
    main()

    GPIO.output(7, False)
    GPIO.output(11, False)
    GPIO.output(12, True)