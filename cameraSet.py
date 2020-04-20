import RPi.GPIO as GPIO
import os

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

selection = 4
enable1 = 1selection
enable2 = 18


GPIO.setup(selection, GPIO.OUT)
GPIO.setup(enable1, GPIO.OUT)
GPIO.setup(enable2, GPIO.OUT)


def main():
    GPIO.output(selection, False)
    GPIO.output(enable1, False)
    GPIO.output(enable2, True)
    capture(1)

    GPIO.output(selection, True)
    GPIO.output(enable1, False)
    GPIO.output(enable2, True)
    capture(2)


def capture(cam):
    cmd = "raspistill -o capture_%d.jpg" % cam
    os.system(cmd)

if __name__ == "__main__":
    main()

    GPIO.output(selection, False)
    GPIO.output(enable1, False)
    GPIO.output(enable2, True)