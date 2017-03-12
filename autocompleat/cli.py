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

print("setup everything")
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

clearScreen = False
###############
#  TABLE CLI  #
###############
@click.group()
def cliTable():
    pass

@cliTable.command('lower')
@click.argument('mm', type=click.FLOAT)
@click.argument('speed', type=click.FloatRange(min=0))
def tableLower(mm, speed):
    tableObj.lower(mm, speed)
    global clearScreen
    clearScreen = True

@cliTable.command('lift')
@click.argument('mm', type=click.FLOAT)
@click.argument('speed', type=click.FloatRange(min=0))
def tableLift(mm, speed):
    tableObj.lift(mm, speed)
    global clearScreen
    clearScreen = True

@cliTable.command('mvabs')
@click.argument('mm', type=click.FloatRange(min=0))
@click.argument('speed', type=click.FloatRange(min=0))
def tableMvabs(mm, speed):
    tableObj.setHeight(mm, speed)
    global clearScreen
    clearScreen = True

@cliTable.command('home')
def tableHome():
    tableObj.home()
    global clearScreen
    clearScreen = True

@cliTable.command('enable')
def tableEnable():
    tableObj.enable()
    global clearScreen
    clearScreen = True

@cliTable.command('disable')
def talbleDisable():
    tableOjb.disable()
    global clearScreen
    clearScreen = True

#############
#  ROD CLI  #
#############

@click.group()
def cliRod():
    pass

cliRodCommandChoice = ['x', 'y']

@cliRod.command('mvrel')
@click.argument('rod', type=click.Choice(cliRodCommandChoice))
@click.argument('mm', type=click.FLOAT)
@click.argument('speed', type=click.FloatRange(min=0))
def rodMvrel(rod, mm, speed):
    rodOjb = rodXObj
    if rod == 'y':
        rodObj = rodYObj
    rodObj.move(mm, speed)
    global clearScreen
    clearScreen = True

@cliRod.command('mvabs')
@click.argument('rod', type=click.Choice(cliRodCommandChoice))
@click.argument('mm', type=click.FloatRange(min=0))
@click.argument('speed', type=click.FloatRange(min=0))
def rodMvabs(rod, mm, speed):
    rodOjb = rodXObj
    if rod == 'y':
        rodObj = rodYObj
    rodObj.setPosition(mm, speed)
    global clearScreen
    clearScreen = True

@cliRod.command('rotate')
@click.argument('rod', type=click.Choice(cliRodCommandChoice))
@click.argument('speed', type=click.FloatRange(min=0))
@click.argument('rotDir', type=click.Choice(['cw', 'ccw']))
def rodRotate(rod, speed, rotDir):
    rodOjb = rodXObj
    if rod == 'y':
        rodObj = rodYObj
    rodRotDir = config.DC_ROT_CW
    if rotDir == 'ccw':
        rodRotDir = config.DC_ROT_CCW
    rodObj.rotate(speed, rodRotDir)
    global clearScreen
    clearScreen = True

@cliRod.command('stop')
@click.argument('rod', type=click.Choice(cliRodCommandChoice))
def rodStop(rod):
    rodOjb = rodXObj
    if rod == 'y':
        rodObj = rodYObj
    rodObj.stop()
    global clearScreen
    clearScreen = True

@cliRod.command('home')
@click.argument('rod', type=click.Choice(cliRodCommandChoice))
def rodHome(rod):
    rodOjb = rodXObj
    if rod == 'y':
        rodObj = rodYObj
    rodObj.home()
    global clearScreen
    clearScreen = True

@cliRod.command('enable')
@click.argument('rod', type=click.Choice(cliRodCommandChoice))
def rodEnable(rod):
    rodOjb = rodXObj
    if rod == 'y':
        rodObj = rodYObj
    rodObj.enable()
    global clearScreen
    clearScreen = True

@cliRod.command('disable')
@click.argument('rod', type=click.Choice(cliRodCommandChoice))
def rodDisable(rod):
    rodOjb = rodXObj
    if rod == 'y':
        rodObj = rodYObj
    rodObj.disable()
    global clearScreen
    clearScreen = True

##############
#  TAPE CLI  #
##############
@click.group()
def cliTape():
    pass

cliTapeCommandChoice = ['xl', 'xr', 'y']

@cliTape.command('mvrel')
@click.argument('tape', type=click.Choice(cliTapeCommandChoice))
@click.argument('mm', type=click.FloatRange(min=0))
@click.argument('speed', type=click.FloatRange(min=0))
def tapeMvrel(tape, mm, speed):
    tapeObj = tapeXLeftObj
    if tape == 'xr':
        tapeObj = tapeXRightObj
    elif tape == 'y':
        tapeObj = tapeYObj
    tapeObj.move(mm, speed)
    global clearScreen
    clearScreen = True

@cliTape.command('mvabs')
@click.argument('tape', type=click.Choice(cliTapeCommandChoice))
@click.argument('mm', type=click.FloatRange(min=0))
@click.argument('speed', type=click.FloatRange(min=0))
def tapeMvabs(tape, mm, speed):
    tapeObj = tapeXLeftObj
    if tape == 'xr':
        tapeObj = tapeXRightObj
    elif tape == 'y':
        tapeObj = tapeYObj
    tapeObj.setPosition(mm, speed)
    global clearScreen
    clearScreen = True

@cliTape.command('ext')
@click.argument('tape', type=click.Choice(cliTapeCommandChoice))
@click.argument('mm', type=click.FloatRange(min=0))
@click.argument('speed', type=click.FloatRange(min=0))
def tapeExt(tape, mm, speed):
    tapeObj = tapeXLeftObj
    if tape == 'xr':
        tapeObj = tapeXRightObj
    elif tape == 'y':
        tapeObj = tapeYObj
    tapeObj.extend(mm, speed)
    global clearScreen
    clearScreen = True

@cliTape.command('ret')
@click.argument('tape', type=click.Choice(cliTapeCommandChoice))
@click.argument('mm', type=click.FloatRange(min=0))
@click.argument('speed', type=click.FloatRange(min=0))
def tapeRet(tape, mm, speed):
    tapeObj = tapeXLeftObj
    if tape == 'xr':
        tapeObj = tapeXRightObj
    elif tape == 'y':
        tapeObj = tapeYObj
    tapeObj.retract(mm, speed)
    global clearScreen
    clearScreen = True

@cliTape.command('extabs')
@click.argument('tape', type=click.Choice(cliTapeCommandChoice))
@click.argument('mm', type=click.FloatRange(min=0))
@click.argument('speed', type=click.FloatRange(min=0))
def tapeExtAbs(tape, mm, speed):
    tapeObj = tapeXLeftObj
    if tape == 'xr':
        tapeObj = tapeXRightObj
    elif tape == 'y':
        tapeObj = tapeYObj
    tapeObj.setExtrusion(mm, speed)
    global clearScreen
    clearScreen = True

@cliTape.command('lift')
@click.argument('tape', type=click.Choice(cliTapeCommandChoice))
@click.argument('mm', type=click.FloatRange(min=0))
def tapeLift(tape, mm):
    tapeObj = tapeXLeftObj
    if tape == 'xr':
        tapeObj = tapeXRightObj
    elif tape == 'y':
        tapeObj = tapeYObj
    # TODO: implement this and the associated functions in class Tape
    click.echo('Currently not available')

@cliTape.command('lower')
@click.argument('tape', type=click.Choice(cliTapeCommandChoice))
@click.argument('mm', type=click.FloatRange(min=0))
def tapeLower(tape, mm):
    tapeObj = tapeXLeftObj
    if tape == 'xr':
        tapeObj = tapeXRightObj
    elif tape == 'y':
        tapeObj = tapeYObj
    # TODO: implement this and the associated functions in class Tape
    click.echo('Currently not available')

@cliTape.command('liftabs')
@click.argument('tape', type=click.Choice(cliTapeCommandChoice))
@click.argument('mm', type=click.FloatRange(min=0))
def tapeLiftAbs(tape, mm):
    tapeObj = tapeXLeftObj
    if tape == 'xr':
        tapeObj = tapeXRightObj
    elif tape == 'y':
        tapeObj = tapeYObj
    tapeObj.setCamHeight(mm)
    global clearScreen
    clearScreen = True

@cliTape.command('home')
@click.argument('tape', type=click.Choice(cliTapeCommandChoice))
def tapeHome(tape):
    tapeObj = tapeXLeftObj
    if tape == 'xr':
        tapeObj = tapeXRightObj
    elif tape == 'y':
        tapeObj = tapeYObj
    tapeObj.home()
    global clearScreen
    clearScreen = True

@cliTape.command('enable')
@click.argument('tape', type=click.Choice(cliTapeCommandChoice))
def tapeEnable(tape):
    tapeObj = tapeXLeftObj
    if tape == 'xr':
        tapeObj = tapeXRightObj
    elif tape == 'y':
        tapeObj = tapeYObj
    tapeObj.enable()
    global clearScreen
    clearScreen = True

@cliTape.command('disable')
@click.argument('tape', type=click.Choice(cliTapeCommandChoice))
def tapeDisable(tape):
    tapeObj = tapeXLeftObj
    if tape == 'xr':
        tapeObj = tapeXRightObj
    elif tape == 'y':
        tapeObj = tapeYObj
    tapeObj.disable()
    global clearScreen
    clearScreen = True

#########
#  CLI  #
#########
def printInformation():
    tablePos = tableObj.getHeight()
    rodXPos = rodXObj.getPosition()
    rodYPos = rodYObj.getPosition()
    tapeCarrXLeftPos = tapeXLeftObj.getPosition()
    tapeXLeftPos = tapeXLeftObj.getTapePosition()
    tapeXLeftHeight = tapeXLeftObj.getTapeHeight()
    tapeCarrXRightPos = tapeXRightObj.getPosition()
    tapeXRightPos = tapeXRightObj.getTapePosition()
    tapeXRightHeight = tapeXRightObj.getTapeHeight()
    tapeCarrYPos = tapeYObj.getPosition()
    tapeYPos = tapeYObj.getTapePosition()
    tapeYHeight = tapeYObj.getTapeHeight()

    click.echo(click.style('autocompleat CLI', fg='green'))
    click.echo(click.style('Table Height:                %f mm' % tablePos))
    click.echo(click.style('Rod X Carriage Position:     %f mm' % rodXPos))
    click.echo(click.style('Rod Y Carriage Position:     %f mm' % rodYPos))
    click.echo('')

    click.echo(click.style('Tape XL Carraige Position:   %f mm' % tapeCarrXLeftPos))
    click.echo(click.style('Tape XL Position:            %f mm' % tapeXLeftPos))
    click.echo(click.style('Tape XL Height:              %f mm' % tapeXLeftHeight))
    click.echo('')

    click.echo(click.style('Tape XR Carraige Position:   %f mm' % tapeCarrXRightPos))
    click.echo(click.style('Tape XR Position:            %f mm' % tapeXRightPos))
    click.echo(click.style('Tape XR Height:              %f mm' % tapeXRightHeight))
    click.echo('')

    click.echo(click.style('Tape Y Carriage Position:    %f mm' % tapeCarrYPos))
    click.echo(click.style('Tape Y Position:             %f mm' % tapeYPos))
    click.echo(click.style('Tape Y Height:               %f mm' % tapeYHeight))

    click.echo("""Commands:
          table
          rod
          tape""")

def cli():
    global clearScreen
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
                cliTable(opt, prog_name='table')
            elif cmd =='rod':
                cliRod(opt, prog_name='rod')
            elif cmd == 'tape':
                cliTape(opt, prog_name='tape')
            elif cmd == 'q':
                break
            else:
                click.echo("Invalid command.")
        except:
            pass

        if clearScreen:
            click.clear()
            printInformation()
            clearScreen = False

if __name__ == "__main__":
    try:
        print("Welcome to the autocompleat CLI")
        cli()
    finally:
        RPi.GPIO.cleanup()
