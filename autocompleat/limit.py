import time

import config

class LimitSwitch(object):

    def __init__(self, mcp, limitPin):
        self.mcp = mcp
        self.limitPin = limitPin

    def isOpen(self):
        return self.mcp.input(self.limitPin) == config.LIMIT_SWITCH_OPEN

    def isClose(self):
        return self.mcp.input(self.limitPin) == config.LIMIT_SWITCH_CLOSE

    def waitUntilClose(self, debounce=0):
        debouncing = True
        debounce = max(0, debounce)

        while debouncing:
            while self.isOpen():
                pass
            debouncing = False
            if debounce:
                time.sleep(debounce)
                if self.isOpen():
                    debouncing = True
        print("Switch is now closed")

