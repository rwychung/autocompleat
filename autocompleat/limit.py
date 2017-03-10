import RPi

class LimitSwitch(object):

    def __init__(self, mcp, intPin, limitPin, callback=None, debounce=0):
        self.limitPin = limitPin
        self.debounce = debounce
        self.callback = callback
        if self.callback:
            self.setCallback(self.callback)

    def setCallback(self, callback):
        self.callback = callback
        RPi.GPIO.add_event_detect(self.intPin, RPi.GPIO.FALLING,
                                  callback=callback, bouncetime=debounce)
