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
        self.curPos = 0
        self.disable()

    def move(self, mm, speed):
        """speed = mm/s"""
        self.curPos += mm
        steps = self._mm2steps(mm) * self.homeDir
        rpm = self._angSpeed2Rpm(speed)
        self.carriage.step(steps, rpm)

    def rotate(self, rpm, rotDir = config.DC_ROT_CW):
        self.rod.rotate(rpm, rotDir)

    def stop(self):
        self.rod.rotate(0)

    def enable(self):
        self.carriage.enable()

    def home(self):
        carrDir = config.STEPPER_ROT_CW
        if self.homeDir == config.HOME_DIR_NEG:
            carrDir = config.STEPPER_ROT_CCW

        # Start homing
        self.carriage.run(carrDir, config.CARR_HOME_RPM)
        self.limitSwitch.waitUntilClose()

        self.disable()
        self.enable()
        self.curPos = 0

    def disable(self):
        self.carriage.disable()
        self.rod.stop()

    def _mm2steps(self, mm):
        return config.CARR_STEPS_PER_MM  * mm

    def _angSpeed2Rpm(self, angSpeed):
        return angSpeed * 60 / config.CARR_STEPS_PER_REV
