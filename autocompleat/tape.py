import RPi

import motor

class Tape(object):

    def __init__(self, carriageMotor, tapeMotor, camMotor, homeDir):
        self.carriage = carriageMotor
        self.tape = tapeMotor
        self.cam = camMotor
        self.homeDir = homeDir

    def move(self, mm, speed):
        steps = self._mm2StepsCarr(mm) * self.homeDir
        rpm = self._angSpeed2RpmCarr(speed)
        self.carriage.step(steps, rpm)

    def extend(self, mm, speed):
        steps = self._mm2StepsTape(mm)
        rpm = self._angSpeed2RpmTape(speed)
        self.tape.step(steps, rpm)

    def retract(self, mm, speed):
        self.extend(-mm, speed)

    def lift(self, mm):
        pos = config.PWM_PULSE_LENGTH
        self.cam.setPos()

    def lower(self, mm):
        # TODO: do some math to conver mm to pos
        pos = config.PWM_PULSE_LENGTH
        self.cam.setPos()

    def home(self, mm, speed):
        pass

    def enable(self):
        self.carriage.enable()
        self.tape.enable()

    def disable(self):
        self.carriage.disable()
        self.tape.disable()

    def _mm2StepsCarr(self, mm):
        return config.CARR_STEPS_PER_MM * mm

    def _angSpeed2RpmCarr(self, angSpeed):
        return angSpeed * 60 / config.CARR_STEPS_PER_REV

    def _mm2StepsTape(self, mm):
        return config.TAPE_STEPS_PER_MM * mm

    def _angSpeed2RpmTape(self, angSpeed):
        return angSpeed * 60 / config.TAPE_STEPS_PER_REV
