import RPi.GPIO as gpio
from time import sleep

gpio.setmode(gpio.BOARD)

motorRa = 16
motorRb = 18
motorRe = 22

motorLa = 36
motorLb = 38
motorLe = 40

gpio.setwarnings(False)

gpio.setup(motorRa, gpio.OUT)
gpio.setup(motorRb, gpio.OUT)
gpio.setup(motorRe, gpio.OUT)

gpio.setup(motorLa, gpio.OUT)
gpio.setup(motorLb, gpio.OUT)
gpio.setup(motorLe, gpio.OUT)

def front():
	gpio.output(motorRa, gpio.HIGH)
	gpio.output(motorRb, gpio.LOW)
	gpio.output(motorRe, gpio.HIGH)

	gpio.output(motorLa, gpio.HIGH)
	gpio.output(motorLb, gpio.LOW)
	gpio.output(motorLe, gpio.HIGH)

def back():
	gpio.output(motorRa, gpio.LOW)
	gpio.output(motorRb, gpio.HIGH)
	gpio.output(motorRe, gpio.HIGH)

	gpio.output(motorLa, gpio.LOW)
	gpio.output(motorLb, gpio.HIGH)
	gpio.output(motorLe, gpio.HIGH)

def stop():
	gpio.output(motorRe, gpio.LOW)
	gpio.output(motorLe, gpio.LOW)

print "Fowards"
front()
sleep(2)

print "Backwards"
back()
sleep(2)
front()

sleep(2)

print "stop motor"
stop()

gpio.cleanup()
