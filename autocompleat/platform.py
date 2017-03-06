import Adafruit_GPIO
import Adafruit_PCA9685

import config
import motor

class Platform(object):

    def __init__(self, leadScrewMotor)
        self.leadScrew = leadScrewMotor
        self.leadScrew.disable()

    def raise(self, mm, speed):
        """speed = mm/s"""
        steps = self._mm2Steps(mm)
        rpm = self._mmPerS2Rpm(speed)
        self.leadScrew.step(steps, rpm, Z_DIR_RAISE)

    def lower(self, mm, speed):
        steps = self._mm2Steps(mm)
        rpm = self._mmPerS2Rpm(speed)
        self.leadScrew.step(steps, rpm, Z_DIR_LOWER)

    def _mm2Steps(self, mm):
        return config.Z_STEPS_PER_MM * mm

    def _mmPerS2Rpm(self, speed):
        return speed / 60 * Z_MM_PER_REV

    def enable(self):
        self.leadScrew.enable()

    def disable(self):
        self.leadScrew.disable()
