
class SG90:
    loc1 = 7.5
    loc2 = 10.5

    def __init__(self, motor_1, motor_2, GPIO):
        self.GPIO = GPIO
        self.pin_motor1 = motor_1
        self.pin_motor2 = motor_2
        self.setting()

    def setting(self):
        try :
            self.GPIO.setup(self.pin_motor1, self.GPIO.OUT)
            self.GPIO.setup(self.pin_motor2, self.GPIO.OUT)

            self.p1 = self.GPIO.PWM(self.pin_motor1, 50)
            self.p2 = self.GPIO.PWM(self.pin_motor2, 50)

            self.p1.start(0)
            self.p2.start(0)

            self.p1.ChangeDutyCycle(self.loc1)
            self.p2.ChangeDutyCycle(self.loc2)

        except KeyboardInterrupt:
            p1.stop()
            p2.stop()

    def write(self, i):
        if i == 0 : # plus
            if self.loc1 != 10.5:
                self.loc1 = self.loc1 + 1
            self.p1.ChangeDutyCycle(self.loc1)
        elif(i == 1): # minus
            if self.loc1 != 5.5:
                self.loc1 = self.loc1 - 1    
            self.p1.ChangeDutyCycle(self.loc1)
        elif(i == 1): # down
            if self.loc2 != 11.5:
                self.loc2 = self.loc2 + 1
            self.p2.ChangeDutyCycle(self.loc2)
        elif(i == 1): # up
            if self.loc2 != 6.5:
                self.loc2 = self.loc2 - 1    
            self.p2.ChangeDutyCycle(self.loc2)