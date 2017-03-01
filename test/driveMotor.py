import RPi.GPIO as GPIO
import time

#['BCM', 'BOARD', 'BOTH', 'FALLING', 'HARD_PWM', 'HIGH', 'I2C', 'IN', 'LOW',
#'OUT', 'PUD_DOWN', 'PUD_OFF', 'PUD_UP', 'PWM', 'RISING', 'RPI_INFO', 'RPI_REVISION',
#'SERIAL', 'SPI', 'UNKNOWN', 'VERSION', '__builtins__', '__doc__', '__file__', '__name__',
#'__package__', '__path__', 'add_event_callback', 'add_event_detect', 'cleanup',
#'event_detected', 'getmode', 'gpio_function', 'input', 'output',
#'remove_event_detect', 'setmode', 'setup', 'setwarnings', 'wait_for_edge']

leadScrewPWMChannel = 9

# Pin numbers are set according to Pi configuration.
pwmPin = 12
dirPin = 11


GPIO.setmode(GPIO.BOARD)

GPIO.setup(dirPin, GPIO.OUT)
GPIO.setup(pwmPin, GPIO.OUT)

# Initialize PWM frequency to 400 Hz (pulses per second).
pwm = GPIO.PWM(pwmPin, 400)

rodCarriageStepsPerMM = 3.33
rodCarriageStepsPerRev = 200

leadScrewStepsPerRev = 200

def mm2Steps(mm):
    return stepsPerMM*mm

def speed2Freq(rpm):
    return stepsPerRev * rpm / 60

# Set direction of motor
GPIO.output(dirPin, GPIO.HIGH)

# Set PWM pulse width. This determines the speed of the motor
dist = 100; # Move 100mm
steps = mm2Steps(dist)
pwm.start(50)

while True:
    time.sleep(2)
    GPIO.output(dirPin, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(dirPin, GPIO.LOW)

GPIO.cleanup()



# test commit
