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
TAPE_MM_PER_REV = 39.7
TAPE_STEPS_PER_REV = 200
PWM_PULSE_LENGTH = 4096

GPIO.setmode(GPIO.BOARD)

# Setup Adafruit PWM servo hat
PWM = Adafruit_PCA9685.PCA9685()

# Setup GPIO to control z axis stepper
GPIO.setup(Z_AXIS_DIR_PIN, GPIO.OUT)
GPIO.setup(Z_AXIS_RESET_PIN, GPIO.OUT)

def mm2Steps(mm):
    return mm / TAPE_MM_PER_REV * TAPE_STEPS_PER_REV

def speed2Freq(rpm):
    return TAPE_STEPS_PER_REV * rpm / 60

pwmFreq = speed2Freq(120)
PWM.set_pwm_freq(pwmFreq)
print("Runnning at %d Hz") % pwmFreq

GPIO.output(Z_AXIS_DIR_PIN, GPIO.LOW)

start = raw_input("Please enter 1 or 0 to start (1 is out, 0 is in) ")
if start == '0':
    GPIO.output(Z_AXIS_DIR_PIN, GPIO.LOW)
    PWM.set_pwn_freq(speed2Freq(120)
if start == '1':
    GPIO.output(Z_AXIS_DIR_PIN, GPIO.HIGH)
    PWM.set_pwn_freq(speed2Freq(350)

while True:

    dist = 10
    print("Number of steps: %d") % mm2Steps(dist)

    """
    # Raise board by 100mm
    GPIO.output(Z_AXIS_DIR_PIN, GPIO.HIGH)
    PWM.set_pwm(Z_AXIS_STEP_PWM_CHANNEL, PWM_PULSE_LENGTH/2, PWM_PULSE_LENGTH/2)
    time.sleep(1 / pwmFreq * mm2Steps(dist))
    """

    # move tape by 10 mm
    PWM.set_pwm(Z_AXIS_STEP_PWM_CHANNEL, 0, PWM_PULSE_LENGTH//2)
    sleep_time = mm2Steps(dist) / pwmFreq
    print("Sleep for %f seconds") % sleep_time
    time.sleep(sleep_time)
    PWM.set_pwm(Z_AXIS_STEP_PWM_CHANNEL, 0, 0)
    a = raw_input("Press enter to decrease height by %f mm: " % dist)
    if a == '0':
        GPIO.output(Z_AXIS_DIR_PIN, GPIO.LOW)
        PWM.set_pwn_freq(speed2Freq(120)
    if a == '1':
        GPIO.output(Z_AXIS_DIR_PIN, GPIO.HIGH)
        PWM.set_pwn_freq(speed2Freq(350)
    if a == 'q':
        break

GPIO.cleanup()
