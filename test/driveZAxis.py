"""
This file tests the raising and lowering of the board.
"""
from __future__ import division
import time

import RPi.GPIO as GPIO
import Adafruit_PCA9685

# PIN
Z_AXIS_GPIO_ADDR = 0x20
Z_AXIS_DIR_PIN = 29
Z_AXIS_RESET_PIN = 31
Z_AXIS_STEP_PWM_CHANNEL = 9

# CONFIG
Z_STEPS_PER_MM = 25
Z_STEPS_PER_REV = 200
PWM_PULSE_LENGTH = 4096

GPIO.setmode(GPIO.BOARD)

# Setup Adafruit PWM servo hat
PWM = Adafruit_PCA9685.PCA9685()

# Setup GPIO to control z axis stepper
GPIO.setup(Z_AXIS_DIR_PIN, GPIO.OUT)
GPIO.setup(Z_AXIS_RESET_PIN, GPIO.OUT)

def mm2Steps(mm):
    return Z_STEPS_PER_MM * mm

def speed2Freq(rpm):
    return Z_STEPS_PER_REV * rpm / 60

pwmFreq = speed2Freq(120)
PWM.set_pwm_freq(pwmFreq)
print("Runnning at %d Hz") % pwmFreq

GPIO.output(Z_AXIS_DIR_PIN, GPIO.LOW)

start = raw_input("Press enter to start ")
if start == '0':
        GPIO.output(Z_AXIS_DIR_PIN, GPIO.LOW)
if start == '1':
    GPIO.output(Z_AXIS_DIR_PIN, GPIO.HIGH)

while True:

    dist = 10
    print("Number of steps: %d") % mm2Steps(dist)

    """
    # Raise board by 100mm
    GPIO.output(Z_AXIS_DIR_PIN, GPIO.HIGH)
    PWM.set_pwm(Z_AXIS_STEP_PWM_CHANNEL, PWM_PULSE_LENGTH/2, PWM_PULSE_LENGTH/2)
    time.sleep(1 / pwmFreq * mm2Steps(dist))
    """

    # Lower board by 100mm
    PWM.set_pwm(Z_AXIS_STEP_PWM_CHANNEL, 0, PWM_PULSE_LENGTH//2)
    sleep_time = mm2Steps(dist) / pwmFreq
    print("Sleep for %f seconds") % sleep_time
    time.sleep(sleep_time)
    PWM.set_pwm(Z_AXIS_STEP_PWM_CHANNEL, 0, 0)
    a = raw_input("Press enter to decrease height by %f mm: " % dist)
    if a == '0':
        GPIO.output(Z_AXIS_DIR_PIN, GPIO.LOW)
    if a == '1':
        GPIO.output(Z_AXIS_DIR_PIN, GPIO.HIGH)
    if a == 'q':
        break

GPIO.cleanup()
