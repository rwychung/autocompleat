from __future__ import division

import Adafruit_GPIO
import Adafruit_PCA9685

import config
import motor

class Table(object):

    def __init__(self, leadScrewMotor, limitSwitch, homeDir):
        self.leadScrew = leadScrewMotor
        self.leadScrew.disable()
        self.limitSwitch = limitSwitch
        self.limitSwitch.setCallback(self._limitHitCallback)
        self.homeDir = homeDir
        self.curPos = 0

    def lift(self, mm, speed):
        self.curPos += mm
        steps = self._mm2Steps(mm)
        rpm = self._speed2Rpm(speed)
        print("Table rpm: %f" % rpm)
        self.leadScrew.step(steps, rpm)

    def lower(self, mm, speed):
        self.lift(-mm, speed)

    def setHeight(self, mm, speed):
        mm2Go = mm - self.curPos
        self.lift(mm2Go, speed)

    def enable(self):
        self.leadScrew.enable()

    def disable(self):
        self.leadScrew.disable()

    def home(self):
        self.lower(config.MACHINE_HEIGHT, config.TABLE_HOME_RPM)

    def _mm2Steps(self, mm):
        return config.TABLE_STEPS_PER_MM * mm

    def _speed2Rpm(self, speed):
        return speed * 60 / config.TABLE_MM_PER_REV

    def _limitHitCallback(self, channel):
        self.disable()
        self.enable()
        self.curPos = 0
        print("LOL printing callback from channel: %d" % channel)
