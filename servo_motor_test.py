import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD) # numbering system based on board of the RasPI
GPIO.setup(7, GPIO.OUT) # set pin 7 on the board as the one sending PWM/signals to the motor
servo = GPIO.PWM(7,50) # basically say that servo is on pin 7 and send pulse frequency of 50
servo.start(0) # start with 0 duty pulses

# rotate the servo motor -90 degrees
""" servo.ChangeDutyCycle(7)
time.sleep(1) """

# rotate the servo motor 90 degrees
servo.ChangeDutyCycle(7)
time.sleep(1)

# reset the servo motor to neutral position
servo.ChangeDutyCycle(0)
servo.stop()
GPIO.cleanup()
print ("Everything's cleaned up")
