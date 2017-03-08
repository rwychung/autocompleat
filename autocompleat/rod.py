import Adafruit_GPIO
import Adafruit_PCA9685

import config
import motor

class Rod(object):

    def __init__(self, carriageMotor, rodMotor, limitSwitch, homeDir):
        self.carriage = carriageMotor
        self.rod = rodMotor
        self.limit = limitSwitch
        self.homeDir = homeDir

        # Setup limit switch interrupt here
        pass

    def move(self, mm, speed):
        """speed = mm/s"""
        steps = self._mm2steps(mm*homeDir)
        rpm = self._angVel2Rpm(speed)
        self.carriage.step(steps, rpm)

    def startSpin(self, spinDir, speed):
        pass

    def stopSpin(self):
        pass

    def home(self):
        self.move(config.MACHINE_LENGTH, 1)
        #

    def _mm2steps(self, mm):
        return config.CARR_STEPS_PER_MM  * mm

    def _angVel2Rpm(self, angVel):
        return angSpeed * 60 * config.CARR_STEPS_PER_REV
