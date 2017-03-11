from __future__ import division

import Adafruit_GPIO
import Adafruit_PCA9685

import config
import motor

class Rod(object):

    def __init__(self, carriageMotor, rodMotor, limitSwitch, homeDir):
        self.carriage = carriageMotor
        self.rod = rodMotor
        self.limitSwitch = limitSwitch
        self.homeDir = homeDir
        self.disable()

    def move(self, mm, speed):
        """speed = mm/s"""
        steps = self._mm2steps(mm) * self.homeDir
        rpm = self._angSpeed2Rpm(speed)
        self.carriage.step(steps, rpm)

    def rotate(self, rpm, rotDir = config.DC_ROT_CW):
        self.rod.rotate(rpm, rotDir)

    def stop(self):
        self.rod.rotate(0)

    def home(self):
        self.move(config.MACHINE_LENGTH, 1)

    def enable(self):
        self.carriage.enable()

    def disable(self):
        self.carriage.disable()
        self.rod.stop()

    def _mm2steps(self, mm):
        return config.CARR_STEPS_PER_MM  * mm

    def _angSpeed2Rpm(self, angSpeed):
        return angSpeed * 60 / config.CARR_STEPS_PER_REV
