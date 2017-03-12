from __future__ import division

import RPi

# Gantry constants
MACHINE_LENGTH = 1000
MACHINE_HEIGHT = 500

TAPE_CAM_LENGTH = 30

# PWM chip constants
PWM_PULSE_LENGTH = 4095
DEFAULT_PWM_FREQ = 60

# Component enable or disable constants
ENABLED = 1
DISABLED = 0

# Motor configuration constants
STEPPER_ENABLE = RPi.GPIO.HIGH
STEPPER_DISABLE = RPi.GPIO.LOW
STEPPER_ROT_CW = RPi.GPIO.HIGH
STEPPER_ROT_CCW = RPi.GPIO.LOW

DC_MAX_RPM = 100
DC_ROT_CW = RPi.GPIO.HIGH
DC_ROT_CCW = RPi.GPIO.LOW

SERVO_MIN_ROT = 0
SERVO_MAX_ROT = 180
SERVO_MIN_PULSE = 153
SERVO_MAX_PULSE = 640
SERVO_PWM_FREQ = 60
SERVO_TRANS_TIME = 1

# Stepper motor component configurations
TABLE_STEPS_PER_MM = 25
TABLE_STEPS_PER_REV = 200
TABLE_MM_PER_REV = TABLE_STEPS_PER_REV / TABLE_STEPS_PER_MM

CARR_STEPS_PER_MM = 3.33
CARR_STEPS_PER_REV = 200
CARR_MM_PER_REV = CARR_STEPS_PER_REV / CARR_STEPS_PER_MM

TAPE_STEPS_PER_MM = 3.33
TAPE_STEPS_PER_REV = 200
TAPE_MM_PER_REV = TAPE_STEPS_PER_REV / TAPE_STEPS_PER_MM

# Homing configuration
HOME_DIR_POS = 1
HOME_DIR_NEG = -1

TABLE_HOME_DIR = HOME_DIR_NEG
TABLE_HOME_OFFSET = 5
TABLE_HOME_RPM = 1

ROD_X_AXIS_HOME_DIR = HOME_DIR_POS
ROD_Y_AXIS_HOME_DIR = HOME_DIR_POS
ROD_HOME_OFFSET = 5
ROD_HOME_RPM = 1

TAPE_X_AXIS_LEFT_HOME_DIR = HOME_DIR_POS
TAPE_X_AXIS_RIGHT_HOME_DIR = HOME_DIR_NEG
TAPE_Y_AXIS_HOME_DIR = HOME_DIR_POS
TAPE_HOME_OFFSET = 5
TAPE_HOME_RPM = 1

# Push button configuration
PUSH_BUTTON_RELEASED = RPi.GPIO.HIGH
PUSH_BUTTON_PRESSED = RPi.GPIO.LOW

# Limit switch configuration
LIMIT_SWITCH_OPEN = RPi.GPIO.HIGH
LIMIT_SWITCH_CLOSE = RPi.GPIO.LOW
