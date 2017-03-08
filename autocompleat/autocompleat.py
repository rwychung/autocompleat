import RPi
import Adafruit_GPIO.MCP230xx
import Adafruit_PCA9685.PCA9685

import pins
import config

import motor
import table

def startEventLoop():
    # Create MCP and PWM hat objects

    mcpList = [Adafruit_GPIO.MCP230xx.MCP23017(address = addr, busnum = 1) for addr in pins.MCP23017_ADDR]
    pwm = Adafruit_PCA9685.PCA9685(pins.PWM_HAT_ADDR)

    # Initialize pins of MCP
    for i, mcp in enumerate(mcpList):
        for j in range(mcp.NUM_GPIO):
            mcp.setup(j, pins.MCP23017_PINS[i][j])
            if pins.MCP23017_PINS[i][j] == RPi.GPIO.IN:
                mcp.pullup(j, True)

    # Create motor objects
    leadScrewMotor = motor.StepperMotor(mcpList[pins.Z_AXIS_MCP],
                                        pwm,
                                        pins.Z_AXIS_DIR_PIN,
                                        pins.Z_AXIS_RESET_PIN,
                                        pins.Z_AXIS_STEP_PWM_CHANNEL,
                                        config.Z_STEPS_PER_REV)

    # Create component objects
    tableObj = table.Table(leadScrewMotor)

    # Enable components
    tableObj.enable()

    while True:
        dist = 10
        a = raw_input("Press enter to decrease height by %f mm: " % dist)
        if a == '0':
            tableObj.lower(dist, 1)
        if a == '1':
            tableObj.lift(dist, 1)
        if a == 'q':
            break
        pass

if __name__ == "__main__":
    print("Starting autocompleat event loop...")
    RPi.GPIO.setmode(RPi.GPIO.BOARD)
    startEventLoop()
    RPi.GPIO.cleanup()
