from __future__ import division
import time
import wrapt

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
        self.pwm.set_pwm(self.pwmChannel, 0, 0)
        self.mcp.output(self.resetPin, config.STEPPER_ENABLE)

    def disable(self):
        self.mcp.output(self.resetPin, config.STEPPER_DISABLE)
        self.pwm.set_pwm(self.pwmChannel, 0, 0)

    def run(self, stepDir, rpm):
        # Set direction
        self.mcp.output(self.dirPin, stepDir)

        # Make sure rpm is not negative
        rpm = abs(rpm)
        # Saturate rpm
        rpm = min(rpm, config.STEPPER_MAX_RPM)

        # Set PWM freq
        pwmFreq = self._rpm2Freq(rpm)
        print("Rpm: %f" % rpm)
        self.pwm.set_pwm_freq(pwmFreq)
        print("PWM freq: %f" % pwmFreq)
        self.pwm.set_pwm(self.pwmChannel, 0, config.PWM_PULSE_LENGTH//2)

    def step(self, steps, rpm):
        stepDir = config.STEPPER_ROT_CW
        if steps < 0:
            stepDir = config.STEPPER_ROT_CCW

        # Set direction
        self.mcp.output(self.dirPin, stepDir)

        # Make sure rpm is not negative
        rpm = abs(rpm)
        # Saturate rpm
        rpm = min(rpm, config.STEPPER_MAX_RPM)

        # Set PWM freq
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

    def __init__(self, pwm, pwmChannel,
                 minPulseLength, maxPulseLength,
                 pwmFreq = config.SERVO_PWM_FREQ,
                 transTime = config.SERVO_TRANS_TIME):
        self.pwm = pwm
        self.pwmChannel = pwmChannel
        self.minPulseLength = minPulseLength
        self.maxPulseLength = maxPulseLength
        self.pwmFreq = pwmFreq
        self.servoTransTime = transTime
        self.setRot(config.SERVO_MIN_ROT)

    def setRot(self, rot):
        # Saturates position
        if rot < config.SERVO_MIN_ROT:
            rot = config.SERVO_MIN_ROT
        if rot > config.SERVO_MAX_ROT:
            rot = config.SERVO_MAX_ROT

        print("Servo pwm channel: %f" % self.pwmChannel)
        print("Servo pwm freq: %f" % self.pwmFreq)
        print("Servo rot: %f degrees" % rot)

        pulses = int(rot / config.SERVO_MAX_ROT * (self.maxPulseLength - self.minPulseLength)
                     + self.minPulseLength)

        print("Servo pulse: %f" % pulses)

        self.pwm.set_pwm_freq(self.pwmFreq)
        self.pwm.set_pwm(self.pwmChannel, 0, pulses)

        # TODO: Calculate time the servo needs to sleep for
        # Currently sleeps for the maximum time needed to go from min to max position
        print("Servo sleep for: %f second" % self.servoTransTime)
        time.sleep(self.servoTransTime)

class DCMotor(object):

    def __init__(self, mcp, pwm, dirPin, pwmChannel):
        self.mcp = mcp
        self.pwm = pwm
        self.dirPin = dirPin
        self.pwmChannel = pwmChannel

    def rotate(self, rpm, rotDir = config.DC_ROT_CW):
        # Make sure rpm is positive
        rpm = abs(rpm)
        # Saturage rpm
        rpm = min(rpm, config.DC_MAX_RPM)

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
