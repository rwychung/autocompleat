import config

class LimitSwitch(object):

    def __init__(self, mcp, limitPin):
        self.mcp = mcp
        self.limitPin = limitPin

    def isOpen(self):
        return self.mcp.input(self.limitPin) == config.LIMIT_SWITCH_OPEN

    def isClose(self):
        return self.mcp.input(self.limitPin) == config.LIMIT_SWITCH_CLOSE

    def waitUntilClose(self):
        # TODO: Debouncing
        while self.limitSwitch.isOpen():
            pass
        print("Switch is now closed")

