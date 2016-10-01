
import Rpi.gpio as gpio
from time import sleep

gpio.setmode(gpio.BOARD)

motor1a = 16
motor1b = 18
motor1e = 22


gpio.setup(motor1a, gpio.OUT)
gpio.setup(motor1b, gpio.OUT)
gpio.setup(motor1e, gpio.OUT)

print "Foward"
gpio.output(motor1a, gpio.HIGH)
gpio.output(motor1b, gpio.LOW)
gpio.output(motor1e, gpio.HIGH)

sleep(2)

print "Backwards"
gpio.output(motor1a, gpio.LOW)
gpio.output(motor1b, gpio.LOW)
gpio.output(motor1e, gpio.HIGH)

print "stop motor"
gpio.output(motor1e, gpio.HIGH)

gpio.cleanup()
