from __future__ import division

# Gantry constants
MACHINE_LENGTH = 1000
MACHINE_HEIGHT = 500

# PWM chip constants
PWM_PULSE_LENGTH = 4095
DEFAULT_PWM_FREQ = 60

# Motor configuration constants
STEPPER_ENABLE = 1
STEPPER_DISABLE = 0

DC_MAX_RPM = 100
ROT_CW = 1
ROT_CCW = 0

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

TAPE_CAM_LENGTH = 30

# Homing configuration
HOME_DIR_POS = 1
HOME_DIR_NEG = -1

TABLE_HOME_DIR = HOME_DIR_POS
TABLE_HOME_RPM = 1

ROD_X_AXIS_HOME_DIR = HOME_DIR_POS
ROD_Y_AXIS_HOME_DIR = HOME_DIR_POS
ROD_HOME_RPM = 1

TAPE_X_AXIS_LEFT_HOME_DIR = HOME_DIR_POS
TAPE_X_AXIS_RIGHT_HOME_DIR = HOME_DIR_POS
TAPE_Y_AXIS_HOME_DIR = HOME_DIR_POS
TAPE_HOME_RPM = 1

# Limit switch configuration
LIMIT_SWITCH_DEBOUNCE = 300 # in ms
