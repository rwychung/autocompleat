from __future__ import division
import time

import config

class StepperMotor(object):

    def __init__(self, mcp, pwm, dirPin, resetPin, pwmChannel, stepsPerRev):
        self.mcp = mcp
        self.pwm = pwm
        self.dirPin = dirPin
        self.resetPin = resetPin
        self.stepsPerRev = stepsPerRev
        self.pwmChannel = pwmChannel

    def enable(self):
        self.mcp.output(self.resetPin, config.STEPPER_ENABLE)

    def disable(self):
        self.mcp.output(self.resetPin, config.STEPPER_DISABLE)

    def step(self, steps, rpm):
        stepDir = 0
        if steps < 0:
            stepDir = 1

        # Set direction
        self.mcp.output(self.dirPin, stepDir)

        # Set PWM for stepping
        pwmFreq = self._rpm2Freq(rpm)
        print("Rpm: %f" % rpm)
        self.pwm.set_pwm_freq(pwmFreq)
        print("PWM freq: %f" % pwmFreq)
        self.pwm.set_pwm(self.pwmChannel, 0, config.PWM_PULSE_LENGTH//2)

        # Wait until stepping is done
        sleepTime = abs(steps)/pwmFreq
        print("Steps: %f" % steps)
        print("Sleep for %f seconds" % sleepTime)
        time.sleep(sleepTime)

        # Turn off pwm
        self.pwm.set_pwm(self.pwmChannel, 0, 0)

    def _rpm2Freq(self, rpm):
        return self.stepsPerRev * rpm / 60

class ServoMotor(object):

    def __init__(self, pwm, pwmChannel, pwmFreq = config.SERVO_PWM_FREQ,
                                        transTime = config.SERVO_TRANS_TIME):
        self.pwm = pwm
        self.pwmChannel = pwmChannel
        self.pwmFreq = pwmFreq
        self.pwmTransTime = transTime

    def setPos(self, pos):
        # Saturates position
        pos = min(pos, config.PWM_PULSE_LENGTH)

        self.pwm.set_pwm_freq(self.pwmFreq)
        self.pwm.set_pwm(pos)

        # Calculate time the servo needs to sleep for
        # Currently sleeps for the maximum time needed to go from min to max position
        time.sleep(pwmTransTime)

class DCMotor(object):

    def __init__(self, mcp, pwm, dirPin, pwmChannel):
        self.mcp = mcp
        self.pwm = pwm
        self.dirPin = dirPin
        self.pwmChannel = pwmChannel

    def rotate(self, rpm, rotDir = config.ROT_CW):
        # Make sure rpm is positive
        rpm = abs(rpm)

        # Set direction
        self.mcp.output(self.dirPin, rotDir)
        print("DC motor dir pin %d: %d" % (self.dirPin, rotDir))

        # Set speed
        rpm = min(rpm, config.DC_MAX_RPM)
        print("DC motor rpm: %f" % rpm)
        pwmPulseLength = int(rpm / config.DC_MAX_RPM * config.PWM_PULSE_LENGTH)
        print("PWM pulse length: %f" % pwmPulseLength)
        self.pwm.set_pwm(self.pwmChannel, 0, pwmPulseLength)

    def stop(self):
        self.rotate(0)
