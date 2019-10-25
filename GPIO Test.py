import RPi.GPIO as GPIO
import time
from time import sleep

# GPIO Configuration
GPIO.setmode(GPIO.BCM)
GPIO.setup(27,  GPIO.IN)


while (1):
	print("27: " + str(GPIO.input(27)))

	sleep(1)
GPIO.cleanup()
