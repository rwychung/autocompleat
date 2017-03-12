import RPi
import Adafruit_GPIO.I2C
import Adafruit_GPIO.MCP230xx
import Adafruit_PCA9685.PCA9685
import Adafruit_PureIO.smbus

import click

import pins
import config

import button
import limit
import motor
import rod
import table
import tape

# Setup RPi
RPi.GPIO.setmode(RPi.GPIO.BOARD)

# Create MCP and PWM hat objects
busnum = 1
mcpList = [Adafruit_GPIO.MCP230xx.MCP23017(address = addr, busnum = busnum) for addr in pins.MCP23017_ADDR]
pwm = Adafruit_PCA9685.PCA9685(pins.PWM_HAT_ADDR)

# Initialize pins of MCP
for i, mcp in enumerate(mcpList):
    for j in range(mcp.NUM_GPIO):
        mcp.setup(j, pins.MCP23017_PINS[i][j])
        if pins.MCP23017_PINS[i][j] == RPi.GPIO.IN:
            mcp.pullup(j, True)

# Create button object
startButton = button.PushButton(mcpList[pins.PUSH_BUTTON_MCP], pins.PUSH_BUTTON_PIN)

# Create limit switch objects
tableLimit = limit.LimitSwitch(mcpList[pins.LIMIT_MCP], pins.TABLE_LIMIT_PIN)
rodCarrXLimit = limit.LimitSwitch(mcpList[pins.LIMIT_MCP],
                                  pins.RODCARR_X_AXIS_LIMIT_PIN)
rodCarrYLimit = limit.LimitSwitch(mcpList[pins.LIMIT_MCP],
                                  pins.RODCARR_Y_AXIS_LIMIT_PIN)
tapeCarrXLeftLimit = limit.LimitSwitch(mcpList[pins.LIMIT_MCP],
                                       pins.TAPECARR_X_AXIS_LEFT_LIMIT_PIN)
tapeCarrXRightLimit = limit.LimitSwitch(mcpList[pins.LIMIT_MCP],
                                        pins.TAPECARR_X_AXIS_RIGHT_LIMIT_PIN)
tapeCarrYLimit = limit.LimitSwitch(mcpList[pins.LIMIT_MCP],
                                   pins.TAPECARR_Y_AXIS_LIMIT_PIN)

# Create motor objects
leadScrewMotor = motor.StepperMotor(mcpList[pins.TABLE_MCP],
                                    pwm,
                                    pins.TABLE_DIR_PIN,
                                    pins.TABLE_RST_PIN,
                                    pins.TABLE_STEP_PWM_CHANNEL,
                                    config.TABLE_STEPS_PER_REV)

rodCarrXMotor = motor.StepperMotor(mcpList[pins.RODCARR_MCP],
                                   pwm,
                                   pins.RODCARR_X_AXIS_DIR_PIN,
                                   pins.RODCARR_X_AXIS_RST_PIN,
                                   pins.RODCARR_X_AXIS_STEP_PWM_CHANNEL,
                                   config.CARR_STEPS_PER_REV)
rodCarrYMotor = motor.StepperMotor(mcpList[pins.RODCARR_MCP],
                                   pwm,
                                   pins.RODCARR_Y_AXIS_DIR_PIN,
                                   pins.RODCARR_Y_AXIS_RST_PIN,
                                   pins.RODCARR_Y_AXIS_STEP_PWM_CHANNEL,
                                   config.CARR_STEPS_PER_REV)

rodXMotor = motor.DCMotor(mcpList[pins.ROD_MCP],
                          pwm,
                          pins.ROD_X_AXIS_DIR_PIN,
                          pins.ROD_X_AXIS_STEP_PWM_CHANNEL)
rodYMotor = motor.DCMotor(mcpList[pins.ROD_MCP],
                          pwm,
                          pins.ROD_Y_AXIS_DIR_PIN,
                          pins.ROD_Y_AXIS_STEP_PWM_CHANNEL)

tapeCarrXLeftMotor = motor.StepperMotor(mcpList[pins.TAPECARR_MCP],
                                        pwm,
                                        pins.TAPECARR_X_AXIS_LEFT_DIR_PIN,
                                        pins.TAPECARR_X_AXIS_LEFT_RST_PIN,
                                        pins.TAPECARR_X_AXIS_LEFT_STEP_PWM_CHANNEL,
                                        config.CARR_STEPS_PER_REV)
tapeCarrXRightMotor = motor.StepperMotor(mcpList[pins.TAPECARR_MCP],
                                        pwm,
                                        pins.TAPECARR_X_AXIS_RIGHT_DIR_PIN,
                                        pins.TAPECARR_X_AXIS_RIGHT_RST_PIN,
                                        pins.TAPECARR_X_AXIS_RIGHT_STEP_PWM_CHANNEL,
                                        config.CARR_STEPS_PER_REV)
tapeCarrYMotor = motor.StepperMotor(mcpList[pins.TAPECARR_MCP],
                                   pwm,
                                   pins.TAPECARR_Y_AXIS_DIR_PIN,
                                   pins.TAPECARR_Y_AXIS_RST_PIN,
                                   pins.TAPECARR_Y_AXIS_STEP_PWM_CHANNEL,
                                   config.CARR_STEPS_PER_REV)

tapeXMotors = motor.StepperMotor(mcpList[pins.TAPE_MCP],
                                 pwm,
                                 pins.TAPE_X_AXIS_DIR_PIN,
                                 pins.TAPE_X_AXIS_RST_PIN,
                                 pins.TAPE_X_AXIS_STEP_PWM_CHANNEL,
                                 config.TAPE_STEPS_PER_REV)
tapeYMotor = motor.StepperMotor(mcpList[pins.TAPE_MCP],
                                pwm,
                                pins.TAPE_Y_AXIS_DIR_PIN,
                                pins.TAPE_Y_AXIS_RST_PIN,
                                pins.TAPE_Y_AXIS_STEP_PWM_CHANNEL,
                                config.TAPE_STEPS_PER_REV)

tapeCamXLeftMotor = motor.ServoMotor(pwm, pins.TAPECAM_X_AXIS_LEFT_STEP_PWM_CHANNEL)
tapeCamXRightMotor = motor.ServoMotor(pwm, pins.TAPECAM_X_AXIS_RIGHT_STEP_PWM_CHANNEL)
tapeCamYMotor = motor.ServoMotor(pwm, pins.TAPECAM_Y_AXIS_STEP_PWM_CHANNEL)

# Create component objects
tableObj = table.Table(leadScrewMotor, tableLimit, config.TABLE_HOME_DIR,
                       config.TABLE_MIN_POS, config.TABLE_MAX_POS)
rodXObj = rod.Rod(rodCarrXMotor, rodXMotor, rodCarrXLimit,
                  config.ROD_X_AXIS_HOME_DIR,
                  config.RODCARR_X_MIN_POS, config.RODCARR_X_MAX_POS)
rodYObj = rod.Rod(rodCarrYMotor, rodYMotor, rodCarrYLimit,
                  config.ROD_Y_AXIS_HOME_DIR,
                  config.RODCARR_Y_MIN_POS, config.RODCARR_Y_MAX_POS)
tapeXLeftObj = tape.Tape(tapeCarrXLeftMotor, tapeXMotors, tapeCamXLeftMotor,
                         tapeCarrXLeftLimit, config.TAPE_X_AXIS_LEFT_HOME_DIR,
                         config.TAPECARR_X_LEFT_MIN_POS,
                         config.TAPECARR_X_LEFT_MAX_POS,
                         config.TAPE_MIN_POS,
                         config.TAPE_MAX_POS,
                         config.TAPE_CAM_MIN_POS,
                         config.TAPE_CAM_MAX_POS)
tapeXRightObj = tape.Tape(tapeCarrXRightMotor, tapeXMotors, tapeCamXRightMotor,
                         tapeCarrXRightLimit, config.TAPE_X_AXIS_RIGHT_HOME_DIR,
                         config.TAPECARR_X_RIGHT_MIN_POS,
                         config.TAPECARR_X_RIGHT_MAX_POS,
                         config.TAPE_MIN_POS,
                         config.TAPE_MAX_POS,
                         config.TAPE_CAM_MIN_POS,
                         config.TAPE_CAM_MAX_POS)
tapeYObj = tape.Tape(tapeCarrYMotor, tapeYMotor, tapeCamYMotor,
                     tapeCarrYLimit, config.TAPE_Y_AXIS_HOME_DIR,
                         config.TAPECARR_Y_MIN_POS,
                         config.TAPECARR_Y_MAX_POS,
                         config.TAPE_MIN_POS,
                         config.TAPE_MAX_POS,
                         config.TAPE_CAM_MIN_POS,
                         config.TAPE_CAM_MAX_POS)

# Enable table motors
tableObj.enable()
rodXObj.enable()
rodYObj.enable()
tapeXLeftObj.enable()
tapeXRightObj.enable()
tapeYObj.enable()

def eventLoop():
    while True:
        pass

if __name__ == "__main__":
    try:
        eventLoop()
    finally:
        RPi.GPIO.cleanup()
