import RPi
import Adafruit_GPIO
import Adafruit_PCA9685

import pins
import motor
import platform

def startEventLoop():
    # Create MCP and PWM hat objects

    mcpList = [Adafruit_GPIO.MCP230xx(addr) for addr in pins.MCP23017_ADDR]
    pwm = Adafruit_PCA9685.PCA9685()

    # Initialize pins of MCP
    for i, mcp in enumerate(mcpList):
        for j in mcp.NUM_GPIO:
            mcp.setup(j, pins.MCP23017_PINS[i][j])
            if pins.MCP23017_PINS[i][j] == RPi.GPIO.IN:
                mcp.pullup(j, True)

    # Create motor objects
    leadScrewMotor = motor.StepperMotor(mcp[pins.Z_AXIS_MCP],
                                        pwm,
                                        pins.Z_AXIS_DIR_PIN,
                                        pins.Z_AXIS_RESET_PIN,
                                        pins.Z_AXIS_STEP_PWM_CHANNEL)

    # Create component objects
    platform = platform.Platform(leadScrewMotor)

    # Enable components
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
