import RPi
import Adafruit_GPIO.MCP230xx
import Adafruit_PCA9685.PCA9685

import pins
import config

import motor
import rod
import table
import tape

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
                                        pins.Z_AXIS_RST_PIN,
                                        pins.Z_AXIS_STEP_PWM_CHANNEL,
                                        config.Z_STEPS_PER_REV)

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

    tapeXLeftMotor = motor.StepperMotor(mcpList[pins.TAPE_MCP],
                                        pwm,
                                        pins.TAPE_X_AXIS_LEFT_DIR_PIN,
                                        pins.TAPE_X_AXIS_LEFT_RST_PIN,
                                        pins.TAPE_X_AXIS_LEFT_STEP_PWM_CHANNEL,
                                        config.TAPE_STEPS_PER_REV)
    tapeXRightMotor = motor.StepperMotor(mcpList[pins.TAPE_MCP],
                                         pwm,
                                         pins.TAPE_X_AXIS_RIGHT_DIR_PIN,
                                         pins.TAPE_X_AXIS_RIGHT_RST_PIN,
                                         pins.TAPE_X_AXIS_RIGHT_STEP_PWM_CHANNEL,
                                         config.TAPE_STEPS_PER_REV)
    tapeYMotor = motor.StepperMotor(mcpList[pins.TAPE_MCP],
                                    pwm,
                                    pins.TAPE_Y_AXIS_DIR_PIN,
                                    pins.TAPE_Y_AXIS_RST_PIN,
                                    pins.TAPE_Y_AXIS_STEP_PWM_CHANNEL,
                                    config.TAPE_STEPS_PER_REV)

    tapeCamXLeftMotor = motor.ServoMotor(pwm,
                                           pins.TAPECAM_X_AXIS_LEFT_STEP_PWM_CHANNEL)
    tapeCamXRightMotor = motor.ServoMotor(pwm,
                                            pins.TAPECAM_X_AXIS_RIGHT_STEP_PWM_CHANNEL)
    tapeCamYMotor = motor.ServoMotor(pwm,
                                       pins.TAPECAM_Y_AXIS_STEP_PWM_CHANNEL)

    # Create component objects
    tableObj = table.Table(leadScrewMotor)
    rodXObj = rod.Rod(rodCarrXMotor, rodXMotor, config.ROD_X_AXIS_HOME)
    rodYObj = rod.Rod(rodCarrYMotor, rodYMotor, config.ROD_Y_AXIS_HOME)
    tapeXLeftObj = tape.Tape(tapeCarrXLeftMotor, tapeXLeftMotor, tapeCamXLeftMotor,
                             config.TAPE_X_AXIS_LEFT_HOME)
    tapeXRightObj = tape.Tape(tapeCarrXRightMotor, tapeXRightMotor, tapeCamXRightMotor,
                             config.TAPE_X_AXIS_RIGHT_HOME)
    tapeYObj = tape.Tape(tapeCarrYMotor, tapeYMotor, tapeCamYMotor,
                             config.TAPE_Y_AXIS_HOME)

    # Enable table motors
    tableObj.enable()
    rodXObj.enable()
    rodYObj.enable()
    tapeXLeftObj.enable()
    tapeXRightObj.enable()
    tapeYObj.enable()

    while True:
        ctrl = raw_input("""Control the following:
                          [t - table
                           rx - x rod
                           ry - y rod
                           q - quit]""")
        if ctrl == 't':
            while True:
                dist = 1
                a = raw_input("""
                0 - lift dist of %d
                1 - lower dist of %d
                2 - enable table
                3 - disable table
                """ % (dist, dist))

                if a == '0':
                    tableObj.lift(dist, 1)
                elif a == '1':
                    tableObj.lower(dist, 1)
                elif a == '2':
                    tableObj.enable()
                elif a == '3':
                    tableObj.disable()
                elif a == 'q':
                    break
                else:
                    pass
        elif ctrl == 'rx':
            while True:
                dist = 1
                a = raw_input("""
                0 - move dist of %d clockwise
                1 - move dist of %d counter clockwise
                2 - rotate rod clockwise
                3 - rotate rod counter clockwise
                4 - enable carraige motor
                5 - disable carriage motor
                6 - stop rod
                q - quit""" % (dist, dist))

                if a == '0':
                    rodXObj.move(dist, 1)
                elif a == '1':
                    rodXObj.move(-dist, 1)
                elif a == '2':
                    rodXObj.rotate(config.DC_MAX_RPM, config.ROT_CW)
                elif a == '3':
                    rodXObj.rotate(config.DC_MAX_RPM, config.ROT_CCW)
                elif a == '4':
                    rodXObj.enable()
                elif a == '5':
                    rodXObj.disable()
                elif a == '6':
                    rodXObj.stop()
                elif a == 'q':
                    break
                else:
                    pass
        elif ctrl == 'ry':
            while True:
                dist = 1
                a = raw_input("""
                0 - move dist of %d clockwise
                1 - move dist of %d counter clockwise
                2 - rotate rod clockwise
                3 - rotate rod counter clockwise
                4 - enable carraige motor
                5 - disable carriage motor
                6 - stop rod
                q - quit""" % (dist, dist))

                if a == '0':
                    rodYObj.move(dist, 1)
                elif a == '1':
                    rodYObj.move(-dist, 1)
                elif a == '2':
                    rodYObj.rotate(config.DC_MAX_RPM, config.ROT_CW)
                elif a == '3':
                    rodYObj.rotate(config.DC_MAX_RPM, config.ROT_CCW)
                elif a == '4':
                    rodYObj.enable()
                elif a == '5':
                    rodYObj.disable()
                elif a == '6':
                    rodYObj.stop()
                elif a == 'q':
                    break
                else:
                    pass
        elif ctrl == 'q':
            break
        else:
            pass


if __name__ == "__main__":
    print("Starting autocompleat event loop...")
    RPi.GPIO.setmode(RPi.GPIO.BOARD)
    startEventLoop()
    RPi.GPIO.cleanup()
