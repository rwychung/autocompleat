import config

class PushButton(object):

    def __init__(self, mcp, buttonPin):
        self.mcp = mcp
        self.buttonPin = buttonPin

    def isReleased(self):
        return self.mcp.input(self.buttonPin) == config.PUSH_BUTTON_RELEASED

    def isPressed(self):
        return self.mcp.input(self.buttonPin) == config.PUSH_BUTTON_PRESSED

    def waitForButtonPress(self):
        while self.isReleased():
            pass
        print("Push button was pressed")
        while self.isPressed():
            pass
        print("Push button was released")
