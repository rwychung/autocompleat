import Adafruit_GPIO
import Adafruit_PCA9685

import config
import motor

class Platform(object):

    def __init__(self, mcp, pwm, dirPin, resetPin, pwmChannel):
        self.mcp = mcp
        self.pwm = pwm
        self.motor = motor.StepperMotor(self.mcp, self.pwm, dirPin, resetPin,
                                        pwmChannel, config.Z_STEPS_PER_REV)
        self.motor.disable()

    def raise(self, mm, speed):
        """speed = mm/s"""
        steps = self._mm2Steps(mm)
        rpm = self._mmPerS2Rpm(speed)
        self.motor.step(steps, rpm, Z_DIR_RAISE)

    def lower(self, mm, speed):
        steps = self._mm2Steps(mm)
        rpm = self._mmPerS2Rpm(speed)
        self.motor.step(steps, rpm, Z_DIR_LOWER)

    def _mm2Steps(self, mm):
        return config.Z_STEPS_PER_MM * mm

    def _mmPerS2Rpm(self, speed):
        return speed / 60 * Z_MM_PER_REV

    def enable(self):
        self.motor.enable()

    def disable(self):
        self.motor.disable()
