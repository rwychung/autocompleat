import RPi
import Adafruit_GPIO
import Adafruit_PCA9685

import pins
import platform

def startEventLoop():
    # Create MCP and PWM hat objects
    mcp = [Adafruit_GPIO.MCP230xx(pins.MCP23017_0_ADDR),
           Adafruit_GPIO.MCP230xx(pins.MCP23017_1_ADDR),
           Adafruit_GPIO.MCP230xx(pins.MCP23017_2_ADDR)]
    pwm = Adafruit_PCA9685.PCA9685()

    # Initialize pins of MCP

    # Create component objects
    platform = platform.Platform(mcp[0],
                                 pwm,
                                 pins.Z_AXIS_DIR_PIN,
                                 pins.Z_AXIS_RESET_PIN,
                                 pins.Z_AXIS_STEP_PWM_CHANNEL)
    platform.enable()

    while True:
        dist = 10
        a = raw_input("Press enter to decrease height by %f mm: " % dist)
        if a == '0':
            platform.lower(dist, 1)
        if a == '1':
            platform.raise(dist, 1)
        if q == 'q':
            break
        pass

if __name__ == "__main__":
    print("Starting autocompleat event loop...")
    RPi.GPIO.setmode(RPi.GPIO.BOARD)
    startEventLoop()
    RPi.GPIO.cleanup()
