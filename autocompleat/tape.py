from __future__ import division

import RPi

import config
import motor

class Tape(object):

    def __init__(self, carriageMotor, tapeMotor, camMotor, limitSwitch, homeDir):
        self.carriage = carriageMotor
        self.tape = tapeMotor
        self.cam = camMotor
        self.limitSwitch = limitSwitch
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

    def setCamHeight(self, mm):
        # TODO: do some math to conver mm to pos
        mm = min(mm, config.TAPE_CAM_LENGTH)
        rot = mm/config.TAPE_CAM_LENGTH * config.SERVO_MAX_ROT
        self.cam.setRot(rot)

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
