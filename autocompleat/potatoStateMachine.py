import RPi.GPIO as GPIO
from time import sleep

# initialize GPIOs
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP)

def state1():
    while True:
        print 'state 1'
        
        if (GPIO.input(23) == 1):
            sleep(0.3)
            return state2()
            
def state2():
    while True:
        print 'state 2'
        
        if (GPIO.input(23) == 1):
            sleep(0.3)
            return state1()
            
            #test commit

state1()
