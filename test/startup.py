import RPi.GPIO as GPIO

#['BCM', 'BOARD', 'BOTH', 'FALLING', 'HARD_PWM', 'HIGH', 'I2C', 'IN', 'LOW',
#'OUT', 'PUD_DOWN', 'PUD_OFF', 'PUD_UP', 'PWM', 'RISING', 'RPI_INFO', 'RPI_REVISION',
#'SERIAL', 'SPI', 'UNKNOWN', 'VERSION', '__builtins__', '__doc__', '__file__', '__name__',
#'__package__', '__path__', 'add_event_callback', 'add_event_detect', 'cleanup',
#'event_detected', 'getmode', 'gpio_function', 'input', 'output',
#'remove_event_detect', 'setmode', 'setup', 'setwarnings', 'wait_for_edge']

GPIO.setmode(GPIO.BCM)

pressed = False

GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(18, GPIO.OUT)

while True:
	if(GPIO.input(23) == 1):
		print 1
	elif(GPIO.input(24) == 0):
		print 2
	else:
		print 0

#p = GPIO.PWM(18, 10)
#while True:
	#raw_input('Press key to toggle')
	#print 'start PWM'
	#p.start(50)
	#raw_input('Press key to toggle')
	#print 'stop PWM'
	#p.stop()

GPIO.cleanup()

# test commit
