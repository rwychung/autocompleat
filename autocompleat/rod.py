import Adafruit_GPIO
import Adafruit_PCA9685

import config
import motor

class Rod(object):

    def __init__(self, carriageMotor, rodMotor, homeDir):
        self.carriage = carriageMotor
        self.rod = rodMotor
        self.homeDir = homeDir

    def move(self, mm, speed):
        """speed = mm/s"""
        steps = self._mm2steps(mm*homeDir)
        rpm = self._angVel2Rpm(speed)
        self.carriage.step(steps, rpm)

    def startRot(self, rotDir, rpm):
        self.rod.rotate(rpm, rotDir)

    def stopSpin(self):
        self.rod.rotate(0)

    def home(self):
        self.move(config.MACHINE_LENGTH, 1)

    def _mm2steps(self, mm):
        return config.CARR_STEPS_PER_MM  * mm

    def _angVel2Rpm(self, angVel):
        return angSpeed * 60 / config.CARR_STEPS_PER_REV
