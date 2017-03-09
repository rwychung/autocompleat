from __future__ import division

import Adafruit_GPIO
import Adafruit_PCA9685

import config
import motor

class Table(object):

    def __init__(self, leadScrewMotor):
        self.leadScrew = leadScrewMotor
        self.leadScrew.disable()

    def lift(self, mm, speed):
        steps = self._mm2Steps(mm)
        rpm = self._speed2Rpm(speed)
        print("Table rpm: %f" % rpm)
        self.leadScrew.step(steps, rpm)

    def lower(self, mm, speed):
        self.lift(-mm, speed)

    def _mm2Steps(self, mm):
        return config.Z_STEPS_PER_MM * mm

    def _speed2Rpm(self, speed):
        return speed * 60 / config.Z_MM_PER_REV

    def enable(self):
        self.leadScrew.enable()

    def disable(self):
        self.leadScrew.disable()
