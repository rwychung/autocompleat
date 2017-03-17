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

import pdb

# Setup RPi
RPi.GPIO.setmode(RPi.GPIO.BOARD)

# Create MCP and PWM hat objects
busnum = 1
mcpList = [Adafruit_GPIO.MCP230xx.MCP23017(address = addr, busnum = busnum) for addr in pins.MCP23017_ADDR]
stepperPWM = Adafruit_PCA9685.PCA9685(pins.STEPPER_PWM_HAT_ADDR)
servoPWM = Adafruit_PCA9685.PCA9685(pins.SERVO_PWM_HAT_ADDR)

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
                                    stepperPWM,
                                    pins.TABLE_DIR_PIN,
                                    pins.TABLE_RST_PIN,
                                    pins.TABLE_STEP_PWM_CHANNEL,
                                    config.TABLE_STEPS_PER_REV)

rodCarrXMotor = motor.StepperMotor(mcpList[pins.RODCARR_MCP],
                                   stepperPWM,
                                   pins.RODCARR_X_AXIS_DIR_PIN,
                                   pins.RODCARR_X_AXIS_RST_PIN,
                                   pins.RODCARR_X_AXIS_STEP_PWM_CHANNEL,
                                   config.CARR_STEPS_PER_REV)
rodCarrYMotor = motor.StepperMotor(mcpList[pins.RODCARR_MCP],
                                   stepperPWM,
                                   pins.RODCARR_Y_AXIS_DIR_PIN,
                                   pins.RODCARR_Y_AXIS_RST_PIN,
                                   pins.RODCARR_Y_AXIS_STEP_PWM_CHANNEL,
                                   config.CARR_STEPS_PER_REV)

rodXMotor = motor.DCMotor(mcpList[pins.ROD_MCP],
                          stepperPWM,
                          pins.ROD_X_AXIS_DIR_PIN,
                          pins.ROD_X_AXIS_STEP_PWM_CHANNEL)
rodYMotor = motor.DCMotor(mcpList[pins.ROD_MCP],
                          stepperPWM,
                          pins.ROD_Y_AXIS_DIR_PIN,
                          pins.ROD_Y_AXIS_STEP_PWM_CHANNEL)

tapeCarrXLeftMotor = motor.StepperMotor(mcpList[pins.TAPECARR_MCP],
                                        stepperPWM,
                                        pins.TAPECARR_X_AXIS_LEFT_DIR_PIN,
                                        pins.TAPECARR_X_AXIS_LEFT_RST_PIN,
                                        pins.TAPECARR_X_AXIS_LEFT_STEP_PWM_CHANNEL,
                                        config.CARR_STEPS_PER_REV)
tapeCarrXRightMotor = motor.StepperMotor(mcpList[pins.TAPECARR_MCP],
                                        stepperPWM,
                                        pins.TAPECARR_X_AXIS_RIGHT_DIR_PIN,
                                        pins.TAPECARR_X_AXIS_RIGHT_RST_PIN,
                                        pins.TAPECARR_X_AXIS_RIGHT_STEP_PWM_CHANNEL,
                                        config.CARR_STEPS_PER_REV)
tapeCarrYMotor = motor.StepperMotor(mcpList[pins.TAPECARR_MCP],
                                   stepperPWM,
                                   pins.TAPECARR_Y_AXIS_DIR_PIN,
                                   pins.TAPECARR_Y_AXIS_RST_PIN,
                                   pins.TAPECARR_Y_AXIS_STEP_PWM_CHANNEL,
                                   config.CARR_STEPS_PER_REV)

tapeXMotors = motor.StepperMotor(mcpList[pins.TAPE_MCP],
                                 stepperPWM,
                                 pins.TAPE_X_AXIS_DIR_PIN,
                                 pins.TAPE_X_AXIS_RST_PIN,
                                 pins.TAPE_X_AXIS_STEP_PWM_CHANNEL,
                                 config.TAPE_STEPS_PER_REV)
tapeYMotor = motor.StepperMotor(mcpList[pins.TAPE_MCP],
                                stepperPWM,
                                pins.TAPE_Y_AXIS_DIR_PIN,
                                pins.TAPE_Y_AXIS_RST_PIN,
                                pins.TAPE_Y_AXIS_STEP_PWM_CHANNEL,
                                config.TAPE_STEPS_PER_REV)

tapeCamXLeftMotor = motor.ServoMotor(servoPWM, pins.TAPECAM_X_AXIS_LEFT_STEP_PWM_CHANNEL,
                                     config.TAPE_X_LEFT_SERVO_MIN_PULSE,
                                     config.TAPE_X_LEFT_SERVO_MAX_PULSE)
tapeCamXRightMotor = motor.ServoMotor(servoPWM, pins.TAPECAM_X_AXIS_RIGHT_STEP_PWM_CHANNEL,
                                     config.TAPE_X_RIGHT_SERVO_MIN_PULSE,
                                     config.TAPE_X_RIGHT_SERVO_MAX_PULSE)
tapeCamYMotor = motor.ServoMotor(servoPWM, pins.TAPECAM_Y_AXIS_STEP_PWM_CHANNEL,
                                 config.TAPE_Y_SERVO_MIN_PULSE,
                                 config.TAPE_Y_SERVO_MAX_PULSE)

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
                         config.TAPE_HOME_DIR,
                         config.TAPECARR_X_LEFT_MIN_POS,
                         config.TAPECARR_X_LEFT_MAX_POS,
                         config.TAPE_MIN_POS,
                         config.TAPE_MAX_POS,
                         config.TAPE_CAM_MIN_POS,
                         config.TAPE_CAM_MAX_POS)
tapeXRightObj = tape.Tape(tapeCarrXRightMotor, tapeXMotors, tapeCamXRightMotor,
                         tapeCarrXRightLimit, config.TAPE_X_AXIS_RIGHT_HOME_DIR,
                         config.TAPE_HOME_DIR, 
                         config.TAPECARR_X_RIGHT_MIN_POS,
                         config.TAPECARR_X_RIGHT_MAX_POS,
                         config.TAPE_MIN_POS,
                         config.TAPE_MAX_POS,
                         config.TAPE_CAM_MIN_POS,
                         config.TAPE_CAM_MAX_POS)
tapeYObj = tape.Tape(tapeCarrYMotor, tapeYMotor, tapeCamYMotor,
                     tapeCarrYLimit, config.TAPE_Y_AXIS_HOME_DIR,
                         config.TAPE_HOME_DIR,
                         config.TAPECARR_Y_MIN_POS,
                         config.TAPECARR_Y_MAX_POS,
                         config.TAPE_MIN_POS,
                         config.TAPE_MAX_POS,
                         config.TAPE_CAM_MIN_POS,
                         config.TAPE_CAM_MAX_POS)

def homeAll():
    for obj in [tableObj, rodXObj, rodYObj, tapeXLeftObj, tapeXRightObj, tapeYObj]:
        obj.enable()
        obj.home()
        obj.disable()
        
    for obj in [tapeXLeftObj, tapeXRightObj, tapeYObj]:
        obj.setTapeHeight(0)
        
def disableAll():
    for obj in [tableObj, rodXObj, rodYObj, tapeXLeftObj, tapeXRightObj, tapeYObj]:
        obj.disable()

def stopAllRotates():
    for obj in [rodXObj, rodYObj]:
        obj.rotate(0, config.DC_ROT_CW)
        
def firstTwoFolds():
    raw_input('enter to adjust rod to edge of table')

    # move rod to inside edge of table
    rodXObj.enable()
    rodXObj.move(45, 100)
    rodXObj.disable()

    raw_input('enter to lift table up')

    tableObj.enable()
    tableObj.lift(50, 30)
    tableObj.disable()

    raw_input('enter to spin rod')
    rodXObj.rotate(100, config.DC_ROT_CW)

    raw_input('enter to scoop shirt')
    rodXObj.enable()
    rodXObj.move(200, 20)
    rodXObj.disable()

    raw_input('enter to rotate rod slow ccw')
    rodXObj.rotate(50, config.DC_ROT_CCW)

    raw_input('enter to lower table')
    # lower tape
    tableObj.enable()
    tableObj.home()
    tableObj.disable()
    
    raw_input('enter to move tape to fold 1')
    # tape carriage move
    tapeXLeftObj.enable()
    tapeXLeftObj.move(50, 100)

    raw_input('enter to lift tape')
    tapeXLeftObj.liftTape(35)
    tapeXRightObj.liftTape(35)
    
    raw_input('enter to extend tape')
    # tape extend
    tapeXLeftObj.extend(700, 100)
    
    raw_input('enter to lower tape')
    tapeXLeftObj.lowerTape(35)

    raw_input('enter to rotate faster')
    rodXObj.rotate(100, config.DC_ROT_CCW)

    raw_input('enter to bring sleeve over')
    rodXObj.enable()
    rodXObj.move(250, 20)
    rodXObj.disable()
    
    raw_input('enter to retract tape')
    # retract tape xl
    tapeXLeftObj.retract(700, 100)

    raw_input('enter to move rod for fold 2')
    rodXObj.enable()
    rodXObj.setPosition(rodXObj.maxPos, 100)
    rodXObj.disable()

    raw_input('enter to adjust table for fold 2')
    tableObj.enable()
    tableObj.lift(45, 30)
    tableObj.disable()

    raw_input('enter to rotate rod')
    rodXObj.rotate(100, config.DC_ROT_CCW)

    raw_input('enter to scoop sleeve')
    rodXObj.enable()
    rodXObj.move(-220, 20)
    rodXObj.disable()

    raw_input('enter to slow spin rod')
    rodXObj.rotate(50, config.DC_ROT_CW)

    raw_input('enter to drop table')
    # lower tape too
    tableObj.enable()
    tableObj.home()
    tableObj.disable()
    
    raw_input('enter to move tape to fold 2')
    # tape carriage move
    tapeXRightObj.enable()
    tapeXRightObj.move(20, 100)

    raw_input('enter to lift tape')
    tapeXRightObj.liftTape(35)
    tapeXLeftObj.liftTape(35)
    
    raw_input('enter to extend tape')
    # tape extend
    tapeXRightObj.extend(700, 100)
    
    raw_input('enter to lower tape')
    tapeXRightObj.lowerTape(35)

    raw_input('enter to spin rod faster')
    rodXObj.rotate(100, config.DC_ROT_CW)

    raw_input('enter to bring sleeve over')
    rodXObj.enable()
    rodXObj.move(-250, 20)
    rodXObj.disable()
    
    raw_input('enter to retract tape')
    # retract tape xr
    tapeXRightObj.retract(690, 100)
    
    raw_input('enter to home everything before final fold')
    homeAll()
    
def finalFold():
    print '===STARTING FINAL FOLD==='
    
    raw_input('enter to move rod to edge of table')
    rodYObj.enable()
    rodYObj.move(40, 100)
    rodYObj.disable()
    
    raw_input('enter to raise table')
    tableObj.enable()
    tableObj.lift(80, 30)
    tableObj.disable()
    
    raw_input('enter to rotate rod')
    rodYObj.rotate(100, config.DC_ROT_CCW)
    
    raw_input('enter to scoop')
    rodYObj.enable()
    rodYObj.move(125, 30)
    rodYObj.disable()
    
    raw_input('enter to spin rod again')
    rodYObj.rotate(100, config.DC_ROT_CCW)
    
    raw_input('enter to lower table')
    tableObj.enable()
    tableObj.lower(70, 30)
    tableObj.disable()
    
    raw_input('enter to carry shirt')
    rodYObj.enable()
    rodYObj.move(500, 30)
    
    raw_input('enter to rotate other way')
    rodYObj.rotate(100, config.DC_ROT_CW)
    
    raw_input('enter to fold shirt collar')
    rodYObj.move(60, 30)
    rodYObj.rotate(0, config.DC_ROT_CW)
    
    raw_input('enter to home everything')
    homeAll()


def eventLoop():
    while True:
        raw_input('enter to home')

        # initialize

        print "Homing"
        homeAll()

        firstTwoFolds()
        
        finalFold()

        #while(True):
            #raw_input('enter to lift table and servo')
            #tapeYObj.liftTape(20)
            #tableObj.enable()
            #tableObj.lift(35, 30)
            #tableObj.disable()
            #tapeYObj.liftTape(15)
            
            #raw_input('enter to drop table and servo')
            #tapeYObj.lowerTape(20)
            #tableObj.enable()
            #tableObj.lower(35, 30)
            #tableObj.disable()
            #tapeYObj.lowerTape(15)
        
        raw_input('enter to end')
        break



if __name__ == "__main__":
    try:
        eventLoop()
    finally:
        print "Cleaning GPIOs"
        disableAll()
        stopAllRotates()
        RPi.GPIO.cleanup()
