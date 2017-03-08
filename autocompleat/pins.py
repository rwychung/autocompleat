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

##################
#   Pin Layout   #
##################

# Z axis lead screw pin layout
Z_AXIS_MCP = 0
Z_AXIS_DIR_PIN = 14
Z_AXIS_RESET_PIN = 15
Z_AXIS_STEP_PWM_CHANNEL = 9

# Rod carriage pin layout
RODCARR_MCP = 0

RODCARR_X_AXIS_DIR_PIN = 8
RODCARR_X_AXIS_RESET_PIN = 9
RODCARR_X_AXIS_STEP_PWM_CHANNEL = 0

RODCARR_Y_AXIS_DIR_PIN = 12
RODCARR_Y_AXIS_RESET_PIN = 13
RODCARR_Y_AXIS_STEP_PWM_CHANNEL = 2

# Tape measurer carriage pin layout
TAPECARR_MCP = 2

TAPECARR_X_AXIS_LEFT_DIR_PIN = 12
TAPECARR_X_AXIS_LEFT_RESET_PIN = 13
TAPECARR_X_AXIS_LEFT_STEP_PWM_CHANNEL = 8

TAPECARR_X_AXIS_RIGHT_DIR_PIN = 10
TAPECARR_X_AXIS_RIGHT_RESET_PIN = 11
TAPECARR_X_AXIS_RIGHT_STEP_PWM_CHANNEL = 7

TAPECARR_Y_AXIS_DIR_PIN = 8
TAPECARR_Y_AXIS_RESET_PIN = 9
TAPECARR_Y_AXIS_STEP_PWM_CHANNEL = 6

# Tape measurer extender pin layout
TAPE_MCP = 1

TAPE_X_AXIS_LEFT_DIR_PIN = 8
TAPE_X_AXIS_LEFT_RESET_PIN = 9
TAPE_X_AXIS_LEFT_STEP_PWM_CHANNEL = 3

TAPE_X_AXIS_RIGHT_DIR_PIN = 10
TAPE_X_AXIS_RIGHT_RESET_PIN = 11
TAPE_X_AXIS_RIGHT_STEP_PWM_CHANNEL = 4

TAPE_Y_AXIS_DIR_PIN = 12
TAPE_Y_AXIS_RESET_PIN = 13
TAPE_Y_AXIS_STEP_PWM_CHANNEL = 5
