from __future__ import division
import time

import Adafruit_GPIO
import Adafruit_PCA9685

import config

class StepperMotor(object):

    def __init__(self, mcp, pwm, dirPin, resetPin, pwmChannel, stepsPerRev):
        assert type(mcp) is Adafruit_GPIO.MCP230xx
        assert type(pwm) is Adafruit_PCA9685.PCA9685

        self.mcp = mcp
        self.pwm = pwm
        self.dirPin = dirPin
        self.resetPin = resetPin
        self.stepsPerRev = stepsPerRev
        self.pwmChannel = pwmChannel

    def enable(self):
        self.mcp.output(self.resetPin, config.STEPPER_ENABLE)

    def disable(self):
        self.mcp.output(self.resetPin, STEPPER_DISABLE)

    def step(self, steps, rpm, stepDir=0):
        # Set direction
        self.mcp.output(self.dirPin, stepDir)

        # Set PWM for stepping
        pwmFreq = self._rpm2Freq(rpm)
        self.pwm.set_pwm_freq(pwmFreq)
        self.pwm.set_pwm(pwmChannel, 0, config.PWM_PULSE_LENGTH//2)

        # Wait until stepping is done
        sleepTime = steps/pwmFreq
        time.sleep(sleepTime)

        # Turn off pwm
        self.pwm.set_pwm(pwmChannel, 0, 0)

    def _rpm2Freq(rpm):
        return self.stepsPerRev * rpm / 60

class ServoMotor(object):
    pass

class DCMotor(object):
    pass
