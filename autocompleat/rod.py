import Adafruit_GPIO
import Adafruit_PCA9685

import config
import motor

class Rod(object):

    def __init__(self, carriageMotor, rodMotor, limitSwitch):
        self.carriage = carriageMotor
        self.rod = rodMotor
        self.limit = limitSwitch

    def move(self, mm, speed):
        pass

    def startSpin(self, spinDir, speed):
        pass

    def stopSpin(self):
        pass
