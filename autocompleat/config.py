from __future__ import division

# Gantry constants
MACHINE_LENGTH = 1000
MACHINE_HEIGHT = 500

# PWM chip constants
PWM_PULSE_LENGTH = 4096
DEFAULT_PWM_FREQ = 60

# Motor configuration constants
STEPPER_ENABLE = 1
STEPPER_DISABLE = 0
DC_MAX_RPM = 100
ROT_CW = 1
ROT_CCW = 0

Z_STEPS_PER_MM = 25
Z_STEPS_PER_REV = 200
Z_MM_PER_REV = Z_STEPS_PER_REV / Z_STEPS_PER_MM

CARR_STEPS_PER_MM = 3.33
CARR_STEPS_PER_REV = 200
CARR_MM_PER_REV = CARR_STEPS_PER_REV / CARR_STEPS_PER_MM

# Home direction
HOME_DIR_POS = 1
HOME_DIR_NEG = -1

ROD_X_AXIS_HOME = HOME_DIR_POS
ROD_Y_AXIS_HOME = HOME_DIR_POS

