from __future__ import division

import RPi

import config
import motor

class Tape(object):

    def __init__(self, carriageMotor, tapeMotor, camMotor, limitSwitch, homeDir,
                 tapeHomeDir, minPos, maxPos, minTapePos, maxTapePos, minCamPos, maxCamPos):
        self.carriage = carriageMotor
        self.tape = tapeMotor
        self.cam = camMotor
        self.limitSwitch = limitSwitch
        self.homeDir = homeDir
        self.tapeHomeDir = tapeHomeDir
        self.minPos = minPos
        self.maxPos = maxPos
        self.minTapePos = minTapePos
        self.maxTapePos = maxTapePos
        self.minCamPos = minCamPos
        self.maxCamPos = maxCamPos
        self.curPos = 0
        self.curTapePos = 0
        self.curCamPos = 0
        self.state = config.DISABLED
        self.disable()

    def move(self, mm, speed):
        if self.state == config.DISABLED:
            return

        if self.minPos <= (self.curPos + mm) <= self.maxPos:
            self.curPos += mm
            steps = self._mm2StepsCarr(mm) * self.homeDir
            rpm = self._linSpeed2RpmCarr(speed)
            self.carriage.step(steps, rpm)

    def setPosition(self, mm, speed):
        mm = mm - self.curPos
        self.move(mm, speed)

    def extend(self, mm, speed):
        if self.state == config.DISABLED:
            return

        if self.minTapePos <= (self.curTapePos + mm) <= self.maxTapePos:
            self.curTapePos += mm
            steps = self._mm2StepsTape(mm) * self.tapeHomeDir
            rpm = self._linSpeed2RpmTape(speed)
            self.tape.step(steps, rpm)

    def retract(self, mm, speed):
        self.extend(-mm, speed)

    def setExtrusion(self, mm, speed):
        mm = mm - self.curTapePos
        self.extend(mm, speed)

    def liftTape(self, mm):
        if self.minCamPos <= (self.curCamPos + mm) <= self.maxCamPos:
            self.curCamPos += mm
            rot = self._mm2Rotation(self.curCamPos)
            self.cam.setRot(rot)

    def lowerTape(self, mm):
        self.liftTape(-mm)

    def setTapeHeight(self, mm):
        mm = mm - self.curCamPos
        self.liftTape(mm)

    def getPosition(self):
        return self.curPos

    def getTapePosition(self):
        return self.curTapePos

    def getTapeHeight(self):
        return self.curCamPos

    def setTapePosition(self, mm):
        self.curTapePos = mm

    def enable(self):
        self.carriage.enable()
        self.tape.enable()
        self.state = config.ENABLED

    def disable(self):
        self.carriage.disable()
        self.tape.disable()
        self.state = config.DISABLED

    def home(self):
        if self.state == config.DISABLED:
            return

        carrDir = config.STEPPER_ROT_CW
        if self.homeDir == config.HOME_DIR_NEG:
            carrDir = config.STEPPER_ROT_CCW

        # Start homing
        self.carriage.run(carrDir, config.TAPE_HOME_RPM)
        self.limitSwitch.waitUntilClose()

        self.disable()
        self.enable()
        self.curPos = 0

    def _mm2StepsCarr(self, mm):
        return config.CARR_STEPS_PER_MM * mm

    def _linSpeed2RpmCarr(self, linSpeed):
        return self._mm2StepsCarr(linSpeed) * 60 / config.CARR_STEPS_PER_REV

    def _mm2StepsTape(self, mm):
        return config.TAPE_STEPS_PER_MM * mm

    def _linSpeed2RpmTape(self, linSpeed):
        return self._mm2StepsTape(linSpeed) * 60 / config.TAPE_STEPS_PER_REV

    def _mm2Rotation(self, mm):
        return mm / self.maxCamPos * config.SERVO_MAX_ROT
