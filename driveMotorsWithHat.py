import RPi.GPIO as GPIO
import time
from Adafruit_PWM_Servo_Driver import PWM

# Initialize Adafruit Servo/PWM HAT addressed at 0x40 (I2C).
pwmHat = PWM(0x40)

# Define PWM channels.
leadScrewPWMChannel = 9
upperLeftRodPWMChannel = 10

# Define GPIO pins.
dirPin = 11

# Run lead screw steppers:
# Set lead screw PWM to 50% duty cycle.
#pwmHat.setPWM(leadScrewPWMChannel, 0, 2048)

GPIO.setmode(GPIO.BOARD)

GPIO.setup(dirPin, GPIO.OUT)

# Set direction of motor
GPIO.output(dirPin, GPIO.HIGH)

count = 0
while count < 0:
    time.sleep(2)
    GPIO.output(dirPin, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(dirPin, GPIO.LOW)
    count += 1

# Set lead screw PWM to 0% duty cycle.
pwmHat.setPWM(leadScrewPWMChannel, 0, 0)

# Run upper left rod DC motor:
# Alternate upper left rod PWM between 50% and 0% duty cycle.
pwmHat.setPWMFreq(800)
count = 0
while count < 5:
    time.sleep(2)
    pwmHat.setPWM(upperLeftRodPWMChannel, 0, 3072)
    time.sleep(2)
    #pwmHat.setPWM(upperLeftRodPWMChannel, 0, 0)
    count += 1

pwmHat.setPWM(upperLeftRodPWMChannel, 0, 0)

GPIO.cleanup()
