"""
This file tests the raising and lowering of the board.
"""

import time

import RPi.GPIO as GPIO
import Adafruit_PCA9685

import pins
import config

GPIO.setmode(GPIO.BOARD)

# Setup Adafruit PWM servo hat
PWM = Adafruit_PCA9685.PCA9685()

# Setup GPIO to control z axis stepper
GPIO.setup(pins.Z_AXIS_DIR_PIN, GPIO.OUT)
GPIO.setup(pins.Z_AXIS_RESET_PIN, GPIO.OUT)

def mm2Steps(mm):
    return config.Z_STEPS_PER_MM * mm

def speed2Freq(rpm):
    return config.Z_STEPS_PER_REV * rpm / 60

while True:
    pwmFreq = speed2Freq(10)
    PWM.set_pwm_freq(pwmFreq)

    """
    # Raise board by 100mm
    dist = 100
    GPIO.output(pins.Z_AXIS_DIR_PIN, GPIO.HIGH)
    PWM.set_pwm(pins.Z_AXIS_STEP_PWM_CHANNEL, PWM_PULSE_LENGTH/2, PWM_PULSE_LENGTH/2)
    time.sleep(1 / pwmFreq * mm2Steps(dist))
    """

    # Lower board by 100mm
    GPIO.output(pins.Z_AXIS_DIR_PIN, GPIO.LOW)
    PWM.set_pwm(pins.Z_AXIS_STEP_PWM_CHANNEL, PWM_PULSE_LENGTH/2, PWM_PULSE_LENGTH/2)
    time.sleep(1 / pwmFreq * mm2Steps(dist))
    input("Press enter to decrease height by 100mm")

GPIO.cleanup()
