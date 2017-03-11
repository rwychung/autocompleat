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
tableObj = table.Table(leadScrewMotor, tableLimit, config.TABLE_HOME_DIR)
rodXObj = rod.Rod(rodCarrXMotor, rodXMotor, rodCarrXLimit, config.ROD_X_AXIS_HOME_DIR)
rodYObj = rod.Rod(rodCarrYMotor, rodYMotor, rodCarrYLimit,  config.ROD_Y_AXIS_HOME_DIR)
tapeXLeftObj = tape.Tape(tapeCarrXLeftMotor, tapeXMotors, tapeCamXLeftMotor,
                         tapeCarrXLeftLimit, config.TAPE_X_AXIS_LEFT_HOME_DIR)
tapeXRightObj = tape.Tape(tapeCarrXRightMotor, tapeXMotors, tapeCamXRightMotor,
                         tapeCarrXRightLimit, config.TAPE_X_AXIS_RIGHT_HOME_DIR)
tapeYObj = tape.Tape(tapeCarrYMotor, tapeYMotor, tapeCamYMotor,
                     tapeCarrYLimit, config.TAPE_Y_AXIS_HOME_DIR)

# Enable table motors
tableObj.enable()
rodXObj.enable()
rodYObj.enable()
tapeXLeftObj.enable()
tapeXRightObj.enable()
tapeYObj.enable()

###############
#  TABLE CLI  #
###############
@click.group()
def cliTable():
    pass

@cliTable.command('lower')
@click.argument('mm', type=click.FloatRange(min=0))
@click.argument('speed', type=click.FloatRange(min=0))
def tableLower(mm, speed):
    pass

@cliTable.command('lift')
@click.argument('mm', type=click.FloatRange(min=0))
@click.argument('speed', type=click.FloatRange(min=0))
def tableLift(mm, speed):
    pass

@cliTable.command('mvabs')
@click.argument('mm', type=click.FloatRange(min=0))
@click.argument('speed', type=click.FloatRange(min=0))
def tableMvabs(mm, speed):
    pass

@cliTable.command('home')
def tableHome():
    pass

@cliTable.command('enable')
def tableEnable():
    pass

@cliTable.command('disable')
def talbleDisable():
    pass

#############
#  ROD CLI  #
#############

@click.group()
def cliRod():
    pass

cliRodCommandChoice = ['x', 'y']

@cliRod.command('mvrel')
@click.argument('rod', type=click.Choice(cliRodCommandChoice))
@click.argument('mm', type=click.FloatRange(min=0))
@click.argument('speed', type=click.FloatRange(min=0))
def rodMvrel(rod, mm, speed):
    pass

@cliRod.command('mvabs')
@click.argument('rod', type=click.Choice(cliRodCommandChoice))
@click.argument('mm', type=click.FloatRange(min=0))
@click.argument('speed', type=click.FloatRange(min=0))
def rodMvabs(rod, mm, speed):
    pass

@cliRod.command('rotate')
@click.argument('rod', type=click.Choice(cliRodCommandChoice))
@click.argument('speed', type=click.FloatRange(min=0))
def rodRotate(rod, speed):
    pass

@cliRod.command('stop')
@click.argument('rod', type=click.Choice(cliRodCommandChoice))
def rodStop(rod):
    pass

@cliRod.command('home')
@click.argument('rod', type=click.Choice(cliRodCommandChoice))
def rodHome(rod):
    pass

@cliRod.command('enable')
@click.argument('rod', type=click.Choice(cliRodCommandChoice))
def rodEnable(rod):
    pass

@cliRod.command('disable')
@click.argument('rod', type=click.Choice(cliRodCommandChoice))
def rodDisable(rod):
    pass

##############
#  TAPE CLI  #
##############
@click.group()
def cliTape():
    pass

cliTapeCommandChoice = ['xl', 'xr', 'y']

@cliTape.command('mvrel')
@click.argument('rod', type=click.Choice(cliTapeCommandChoice))
@click.argument('mm', type=click.FloatRange(min=0))
@click.argument('speed', type=click.FloatRange(min=0))
def tapeMvrel(rod, mm, speed):
    pass

@cliTape.command('mvabs')
@click.argument('rod', type=click.Choice(cliTapeCommandChoice))
@click.argument('mm', type=click.FloatRange(min=0))
@click.argument('speed', type=click.FloatRange(min=0))
def tapeMvabs(rod, mm, speed):
    pass

@cliTape.command('ext')
@click.argument('rod', type=click.Choice(cliTapeCommandChoice))
@click.argument('mm', type=click.FloatRange(min=0))
@click.argument('speed', type=click.FloatRange(min=0))
def tapeExt(rod, mm, speed):
    pass

@cliTape.command('ret')
@click.argument('rod', type=click.Choice(cliTapeCommandChoice))
@click.argument('mm', type=click.FloatRange(min=0))
@click.argument('speed', type=click.FloatRange(min=0))
def tapeRet(rod, mm, speed):
    pass

@cliTape.command('extabs')
@click.argument('rod', type=click.Choice(cliTapeCommandChoice))
@click.argument('mm', type=click.FloatRange(min=0))
@click.argument('speed', type=click.FloatRange(min=0))
def tapeExtAbs(rod, mm, speed):
    pass

@cliTape.command('lift')
@click.argument('rod', type=click.Choice(cliTapeCommandChoice))
@click.argument('mm', type=click.FloatRange(min=0))
def tapeLift(rod, mm):
    pass

@cliTape.command('lower')
@click.argument('rod', type=click.Choice(cliTapeCommandChoice))
@click.argument('mm', type=click.FloatRange(min=0))
def tapeLower(rod, mm):
    pass

@cliTape.command('liftabs')
@click.argument('rod', type=click.Choice(cliTapeCommandChoice))
@click.argument('mm', type=click.FloatRange(min=0))
def tapeLiftAbs(rod, mm):
    pass

@cliTape.command('home')
@click.argument('rod', type=click.Choice(cliTapeCommandChoice))
def tapeHome(rod):
    pass

@cliTape.command('enable')
@click.argument('rod', type=click.Choice(cliTapeCommandChoice))
def tapeEnable(rod):
    pass

@cliTape.command('disable')
@click.argument('rod', type=click.Choice(cliTapeCommandChoice))
def tapeDisable(rod):
    pass

#########
#  CLI  #
#########
def printInformation():
    print("autocompleat CLI")

def cliHelp():
    print("""Commands:
          table
          rod
          tape""")

def cli():
    prompt = None
    click.clear()
    printInformation()
    while prompt != 'q':
        prompt = click.prompt('')
        parsed = prompt.split()
        cmd = parsed.pop(0)
        opt = parsed

        click.clear()
        printInformation()
        try:
            if cmd == 'table':
                cliTable.main(opt, prog_name='table')
            elif cmd =='rod':
                cliRod(opt, prog_name='rod')
            elif cmd == 'tape':
                cliTape.main(opt, prog_name='tape')
            elif cmd == 'q':
                break
            else:
                cliHelp()
        except:
            pass

#    while True:
#
#        ctrl = raw_input("""
#                         Control the following:
#                            t - table
#                            rx - x rod
#                            ry - y rod
#                            txl - x left tape
#                            txr - x right tape
#                            ty - y tape
#                            b - button
#                            q - quit]""")
#        if ctrl == 't':
#            while True:
#                dist = 1
#                a = raw_input("""
#                0 - lift dist of %d
#                1 - lower dist of %d
#                2 - enable table
#                3 - disable table
#                4 - home
#                """ % (dist, dist))
#
#                if a == '0':
#                    tableObj.lift(dist, 1)
#                elif a == '1':
#                    tableObj.lower(dist, 1)
#                elif a == '2':
#                    tableObj.enable()
#                elif a == '3':
#                    tableObj.disable()
#                elif a == '4':
#                    tableObj.home()
#                elif a == 'q':
#                    break
#                else:
#                    pass
#        elif ctrl == 'rx':
#            while True:
#                dist = 1
#                a = raw_input("""
#                0 - move dist of %d clockwise
#                1 - move dist of %d counter clockwise
#                2 - rotate rod clockwise
#                3 - rotate rod counter clockwise
#                4 - enable carraige motor
#                5 - disable carriage motor
#                6 - stop rod
#                7 - home carriage
#                q - quit""" % (dist, dist))
#
#                if a == '0':
#                    rodXObj.move(dist, 1)
#                elif a == '1':
#                    rodXObj.move(-dist, 1)
#                elif a == '2':
#                    rodXObj.rotate(config.DC_MAX_RPM, config.DC_ROT_CW)
#                elif a == '3':
#                    rodXObj.rotate(config.DC_MAX_RPM, config.DC_ROT_CCW)
#                elif a == '4':
#                    rodXObj.enable()
#                elif a == '5':
#                    rodXObj.disable()
#                elif a == '6':
#                    rodXObj.stop()
#                elif a == '7':
#                    rodXObj.home()
#                elif a == 'q':
#                    break
#                else:
#                    pass
#        elif ctrl == 'ry':
#            while True:
#                dist = 1
#                a = raw_input("""
#                0 - move dist of %d clockwise
#                1 - move dist of %d counter clockwise
#                2 - rotate rod clockwise
#                3 - rotate rod counter clockwise
#                4 - enable carraige motor
#                5 - disable carriage motor
#                6 - stop rod
#                7 - home carriage
#                q - quit""" % (dist, dist))
#
#                if a == '0':
#                    rodYObj.move(dist, 1)
#                elif a == '1':
#                    rodYObj.move(-dist, 1)
#                elif a == '2':
#                    rodYObj.rotate(config.DC_MAX_RPM, config.DC_ROT_CW)
#                elif a == '3':
#                    rodYObj.rotate(config.DC_MAX_RPM, config.DC_ROT_CCW)
#                elif a == '4':
#                    rodYObj.enable()
#                elif a == '5':
#                    rodYObj.disable()
#                elif a == '6':
#                    rodYObj.stop()
#                elif a == '7':
#                    rodYObj.home()
#                elif a == 'q':
#                    break
#                else:
#                    pass
#        elif ctrl == 'txl':
#            while True:
#                dist = 1
#                extDist = 1
#                a = raw_input("""
#                0 - move dist of %d clockwise
#                1 - move dist of %d counter clockwise
#                2 - extend tape dist of %d
#                3 - retract tape dist of %d
#                4 - set cam min position
#                5 - set cam max position
#                6 - enable carraige and tape motor
#                7 - disable carriage and tape motor
#                8 - home carriage
#                q - quit""" % (dist, dist, extDist, extDist))
#
#                if a == '0':
#                    tapeXLeftObj.move(dist, 1)
#                elif a == '1':
#                    tapeXLeftObj.move(-dist, 1)
#                elif a == '2':
#                    tapeXLeftObj.extend(extDist, 1)
#                elif a == '3':
#                    tapeXLeftObj.retract(extDist, 1)
#                elif a == '4':
#                    tapeXLeftObj.setCamHeight(0)
#                elif a == '5':
#                    tapeXLeftObj.setCamHeight(config.TAPE_CAM_LENGTH)
#                elif a == '6':
#                    tapeXLeftObj.enable()
#                elif a == '7':
#                    tapeXLeftObj.disable()
#                elif a == '8':
#                    tapeXLeftObj.home()
#                elif a == 'q':
#                    break
#                else:
#                    pass
#        elif ctrl == 'txr':
#            while True:
#                dist = 1
#                extDist = 1
#                a = raw_input("""
#                0 - move dist of %d clockwise
#                1 - move dist of %d counter clockwise
#                2 - extend tape dist of %d
#                3 - retract tape dist of %d
#                4 - set cam min position
#                5 - set cam max position
#                6 - enable carraige and tape motor
#                7 - disable carriage and tape motor
#                8 - home carriage
#                q - quit""" % (dist, dist, extDist, extDist))
#
#                if a == '0':
#                    tapeXRightObj.move(dist, 1)
#                elif a == '1':
#                    tapeXRightObj.move(-dist, 1)
#                elif a == '2':
#                    tapeXRightObj.extend(extDist, 1)
#                elif a == '3':
#                    tapeXRightObj.retract(extDist, 1)
#                elif a == '4':
#                    tapeXRightObj.setCamHeight(0)
#                elif a == '5':
#                    tapeXRightObj.setCamHeight(config.TAPE_CAM_LENGTH)
#                elif a == '6':
#                    tapeXRightObj.enable()
#                elif a == '7':
#                    tapeXRightObj.disable()
#                elif a == '8':
#                    tapeXRightObj.home()
#                elif a == 'q':
#                    break
#                else:
#                    pass
#        elif ctrl == 'ty':
#            while True:
#                dist = 1
#                extDist = 1
#                a = raw_input("""
#                0 - move dist of %d clockwise
#                1 - move dist of %d counter clockwise
#                2 - extend tape dist of %d
#                3 - retract tape dist of %d
#                4 - set cam min position
#                5 - set cam max position
#                6 - enable carraige and tape motor
#                7 - disable carriage and tape motor
#                8 - home carriage
#                q - quit""" % (dist, dist, extDist, extDist))
#
#                if a == '0':
#                    tapeYObj.move(dist, 1)
#                elif a == '1':
#                    tapeYObj.move(-dist, 1)
#                elif a == '2':
#                    tapeYObj.extend(extDist, 1)
#                elif a == '3':
#                    tapeYObj.retract(extDist, 1)
#                elif a == '4':
#                    tapeYObj.setCamHeight(0)
#                elif a == '5':
#                    tapeYObj.setCamHeight(config.TAPE_CAM_LENGTH)
#                elif a == '6':
#                    tapeYObj.enable()
#                elif a == '7':
#                    tapeYObj.disable()
#                elif a == '8':
#                    tapeYObj.home()
#                elif a == 'q':
#                    break
#                else:
#                    pass
#        elif ctrl == 'b':
#            print("Waiting for button press")
#            startButton.waitForButtonPress()
#        elif ctrl == 'q':
#            break
#        else:
#            pass


if __name__ == "__main__":
    try:
        print("Welcome to the autocompleat CLI")
        cli()
    finally:
        RPi.GPIO.cleanup()
