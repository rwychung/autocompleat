"""
This file contains hardware specific configurations such as:
    1. Pins for specific hardware
    2. I2C address for chips
"""
import RPi.GPIO

#####################
#   I2C Addresses   #
#####################

# MCP23017 board addresses
MCP23017_ADDR = [0x20, 0x21, 0x22]

MCP23017_PINS = [
                     [RPi.GPIO.IN,
                     RPi.GPIO.IN,
                     RPi.GPIO.IN,
                     RPi.GPIO.IN,
                     RPi.GPIO.IN,
                     RPi.GPIO.IN,
                     RPi.GPIO.IN,
                     RPi.GPIO.IN,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT],

                    [RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT],

                     [RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT,
                     RPi.GPIO.OUT]
                 ]

# Adafruit PWM hat address
PWM_HAT_ADDR = 0x40

###################
#   PI Interrupt  #
###################
PI_INT_PIN = 40

##################
#   Pin Layout   #
##################
######## LIMIT SWITCH ########
LIMIT_MCP = 0

########## TABLE ##########
TABLE_MCP = 0

TABLE_DIR_PIN = 14
TABLE_RST_PIN = 15
TABLE_STEP_PWM_CHANNEL = 9
TABLE_LIMIT_PIN = 0

########## ROD ##########
# Rod carriage pin layout
RODCARR_MCP = 0

RODCARR_X_AXIS_DIR_PIN = 8
RODCARR_X_AXIS_RST_PIN = 9
RODCARR_X_AXIS_STEP_PWM_CHANNEL = 0

RODCARR_X_AXIS_LIMIT_PIN = 1

RODCARR_Y_AXIS_DIR_PIN = 10
RODCARR_Y_AXIS_RST_PIN = 11
RODCARR_Y_AXIS_STEP_PWM_CHANNEL = 1
RODCARR_Y_AXIS_LIMIT_PIN = 2

# Rod motor pin layout
ROD_MCP = 2

ROD_X_AXIS_DIR_PIN = 2
ROD_X_AXIS_STEP_PWM_CHANNEL = 13

ROD_Y_AXIS_DIR_PIN = 1
ROD_Y_AXIS_STEP_PWM_CHANNEL = 14

# Tape measurer carriage pin layout
TAPECARR_MCP = 1

TAPECARR_X_AXIS_LEFT_DIR_PIN = 12
TAPECARR_X_AXIS_LEFT_RST_PIN = 13
TAPECARR_X_AXIS_LEFT_STEP_PWM_CHANNEL = 8
TAPECARR_X_AXIS_LEFT_LIMIT_PIN = 3

TAPECARR_X_AXIS_RIGHT_DIR_PIN = 10
TAPECARR_X_AXIS_RIGHT_RST_PIN = 11
TAPECARR_X_AXIS_RIGHT_STEP_PWM_CHANNEL = 7
TAPECARR_X_AXIS_RIGHT_LIMIT_PIN = 4

TAPECARR_Y_AXIS_DIR_PIN = 8
TAPECARR_Y_AXIS_RST_PIN = 9
TAPECARR_Y_AXIS_STEP_PWM_CHANNEL = 6
TAPECARR_Y_AXIS_LIMIT_PIN = 5
# Tape measurer extender pin layout
TAPE_MCP = 2

TAPE_X_AXIS_LEFT_DIR_PIN = 8
TAPE_X_AXIS_LEFT_RST_PIN = 9
TAPE_X_AXIS_LEFT_STEP_PWM_CHANNEL = 3

TAPE_X_AXIS_RIGHT_DIR_PIN = 10
TAPE_X_AXIS_RIGHT_RST_PIN = 11
TAPE_X_AXIS_RIGHT_STEP_PWM_CHANNEL = 4

TAPE_Y_AXIS_DIR_PIN = 12
TAPE_Y_AXIS_RST_PIN = 13
TAPE_Y_AXIS_STEP_PWM_CHANNEL = 5

# Tape measurer servo cam pin layout
TAPECAM_X_AXIS_LEFT_STEP_PWM_CHANNEL =  10
TAPECAM_X_AXIS_RIGHT_STEP_PWM_CHANNEL = 11
TAPECAM_Y_AXIS_STEP_PWM_CHANNEL = 12
