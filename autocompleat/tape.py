import RPi

import motor

class Tape(object):

    def __init__(self, carriageMotor, tapeMotor, camMotor, limitSwitch, homeDir):
        self.carriage = carriageMotor
        self.tape = tapeMotor
        self.cam = camMotor
        self.limit = limitSwitch
        self.homeDir = homeDir

    def move(self, mm, speed):
        pass

    def extend(self, mm, speed):
        pass

    def retract(self, mm, speed):
        pass

    def raise(self, mm, speed):
        pass

    def lower(self, mm, speed):
        pass

    def home(self, mm, speed):
        pass
