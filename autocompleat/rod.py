from __future__ import division

import Adafruit_GPIO
import Adafruit_PCA9685

import config
import motor

class Rod(object):

    def __init__(self, carriageMotor, rodMotor, limitSwitch, homeDir, minPos, maxPos):
        self.carriage = carriageMotor
        self.rod = rodMotor
        self.limitSwitch = limitSwitch
        self.homeDir = homeDir
        self.minPos = minPos
        self.maxPos = maxPos
        self.curPos = 0
        self.state = config.ENABLED
        self.disable()

    def move(self, mm, speed):
        if self.state == config.DISABLED:
            return

        if self.minPos <= (self.curPos + mm) <= self.maxPos:
            self.curPos += mm
            steps = self._mm2steps(mm) * self.homeDir
            rpm = self._linSpeed2Rpm(speed)
            self.carriage.step(steps, rpm)

    def setPosition(self, mm, speed):
        mm = mm - self.curPos
        self.move(mm, speed)

    def getPosition(self):
        return self.curPos

    def rotate(self, rpm, rotDir = config.DC_ROT_CW):
        self.rod.rotate(rpm, rotDir)

    def stop(self):
        self.rod.rotate(0)

    def home(self):
        if self.state == config.DISABLED:
            return

        carrDir = config.STEPPER_ROT_CW
        if self.homeDir == config.HOME_DIR_NEG:
            carrDir = config.STEPPER_ROT_CCW

        # Start homing
        self.carriage.run(carrDir, config.ROD_HOME_RPM)
        self.limitSwitch.waitUntilClose()

        self.disable()
        self.enable()
        self.curPos = 0

    def enable(self):
        self.carriage.enable()
        self.state = config.ENABLED

    def disable(self):
        self.carriage.disable()
        self.rod.stop()
        self.state = config.DISABLED

    def _mm2steps(self, mm):
        return config.CARR_STEPS_PER_MM  * mm

    def _linSpeed2Rpm(self, linSpeed):
        return self._mm2steps(linSpeed) * 60 / config.CARR_STEPS_PER_REV
