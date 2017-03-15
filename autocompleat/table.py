from __future__ import division

import Adafruit_GPIO
import Adafruit_PCA9685

import config
import motor

class Table(object):

    def __init__(self, leadScrewMotor, limitSwitch, homeDir, minPos, maxPos):
        self.leadScrew = leadScrewMotor
        self.limitSwitch = limitSwitch
        self.homeDir = homeDir
        self.minPos = minPos
        self.maxPos = maxPos
        self.curPos = 0
        self.state = config.DISABLED
        self.disable()

    def lift(self, mm, speed):
        if self.state == config.DISABLED:
            return

        if self.minPos <= (self.curPos + mm) <= self.maxPos:
            self.curPos += mm
            steps = self._mm2Steps(mm) * config.TABLE_HOME_DIR
            rpm = self._speed2Rpm(speed)
            self.leadScrew.step(steps, rpm)

    def lower(self, mm, speed):
        self.lift(-mm, speed)

    def setHeight(self, mm, speed):
        mm2Go = mm - self.curPos
        self.lift(mm2Go, speed)

    def getHeight(self):
        return self.curPos

    def enable(self):
        self.leadScrew.enable()
        self.state = config.ENABLED

    def disable(self):
        self.leadScrew.disable()
        self.state = config.DISABLED

    def home(self):
        if self.state == config.DISABLED:
            return
            
        if self.limitSwitch.isClose():
            pass
            
        else:
            leadScrewDir = config.STEPPER_ROT_CW
            if self.homeDir == config.HOME_DIR_POS:
                leadScrewDir = config.STEPPER_ROT_CCW

            # Start homing
            self.leadScrew.run(leadScrewDir, config.TABLE_HOME_RPM)
            self.limitSwitch.waitUntilClose()

        self.disable()
        self.enable()
        self.curPos = 0

    def _mm2Steps(self, mm):
        return config.TABLE_STEPS_PER_MM * mm

    def _speed2Rpm(self, speed):
        return speed * 60 / config.TABLE_MM_PER_REV
