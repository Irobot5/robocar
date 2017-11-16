import cherrypy
import signal, os
import RPi.GPIO as GPIO
import time

file = open('WASDrightplace.html')
WASDrightplace = file.read()
file.close()

AIN1 = 2
AIN2 = 3
PWMA = 17

BIN1 = 22
BIN2 = 18
PWMB = 27


# Pin Setup:
GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme
GPIO.setwarnings(False)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)


def handler(signum, frame):  # stop when ctrl-c is recieved
	print
	'Signal handler called with signal', signum
	print
	'exiting'
	GPIO.output(PWMA, GPIO.LOW)
	GPIO.output(PWMB, GPIO.LOW)
	GPIO.cleanup()
	exit(0)


# When recieving ctrl-C
signal.signal(signal.SIGINT, handler)

# variables
leftmotor = GPIO.PWM(PWMA, 50)
rightmotor = GPIO.PWM(PWMB, 50)

class Christianscript(object):
	@cherrypy.expose
	def index(self):
		return WASDrightplace

	@cherrypy.expose
	def forward(self):
		GPIO.output(AIN1, GPIO.LOW)
		GPIO.output(AIN2, GPIO.HIGH)
		GPIO.output(PWMA, GPIO.HIGH)
		GPIO.output(BIN1, GPIO.LOW)
		GPIO.output(BIN2, GPIO.HIGH)
		GPIO.output(PWMB, GPIO.HIGH)
		rightmotor.ChangeDutyCycle(100)#trouble running both motors at exact same speed.
		leftmotor.ChangeDutyCycle(100)
		return WASDrightplace

	@cherrypy.expose
	def forright(self):
		GPIO.output(AIN1, GPIO.LOW)
		GPIO.output(AIN2, GPIO.HIGH)
		GPIO.output(PWMA, GPIO.HIGH)
		GPIO.output(BIN1, GPIO.LOW)
		GPIO.output(BIN2, GPIO.HIGH)
		GPIO.output(PWMB, GPIO.HIGH)
		rightmotor.ChangeDutyCycle(85)
		leftmotor.ChangeDutyCycle(100)
		return WASDrightplace

	@cherrypy.expose
	def forleft(self):
		GPIO.output(AIN1, GPIO.LOW)
		GPIO.output(AIN2, GPIO.HIGH)
		GPIO.output(PWMA, GPIO.HIGH)
		GPIO.output(BIN1, GPIO.LOW)
		GPIO.output(BIN2, GPIO.HIGH)
		GPIO.output(PWMB, GPIO.HIGH)
		rightmotor.ChangeDutyCycle(100)
		leftmotor.ChangeDutyCycle(85)
		return WASDrightplace

	@cherrypy.expose
	def backward(self):
		GPIO.output(AIN1, GPIO.HIGH)
		GPIO.output(AIN2, GPIO.LOW)
		GPIO.output(PWMA, GPIO.HIGH)
		GPIO.output(BIN1, GPIO.HIGH)
		GPIO.output(BIN2, GPIO.LOW)
		GPIO.output(PWMB, GPIO.HIGH)
		rightmotor.ChangeDutyCycle(100)
		leftmotor.ChangeDutyCycle(100)
		return WASDrightplace

	@cherrypy.expose
	def backright(self):
		GPIO.output(AIN1, GPIO.HIGH)
		GPIO.output(AIN2, GPIO.LOW)
		GPIO.output(PWMA, GPIO.HIGH)
		GPIO.output(BIN1, GPIO.HIGH)
		GPIO.output(BIN2, GPIO.LOW)
		GPIO.output(PWMB, GPIO.HIGH)
		rightmotor.ChangeDutyCycle(85)
		leftmotor.ChangeDutyCycle(100)
		return WASDrightplace

	@cherrypy.expose
	def backleft(self):
		GPIO.output(AIN1, GPIO.HIGH)
		GPIO.output(AIN2, GPIO.LOW)
		GPIO.output(PWMA, GPIO.HIGH)
		GPIO.output(BIN1, GPIO.HIGH)
		GPIO.output(BIN2, GPIO.LOW)
		GPIO.output(PWMB, GPIO.HIGH)
		rightmotor.ChangeDutyCycle(100)
		leftmotor.ChangeDutyCycle(85)
		return WASDrightplace

	@cherrypy.expose
	def left(self):
		GPIO.output(AIN1, GPIO.HIGH)
		GPIO.output(AIN2, GPIO.LOW)
		GPIO.output(PWMA, GPIO.HIGH)
		GPIO.output(BIN1, GPIO.LOW)
		GPIO.output(BIN2, GPIO.HIGH)
		GPIO.output(PWMB, GPIO.HIGH)
		rightmotor.ChangeDutyCycle(30)
		leftmotor.ChangeDutyCycle(30)
		return WASDrightplace

	@cherrypy.expose
	def right(self):
		GPIO.output(AIN1, GPIO.LOW)
		GPIO.output(AIN2, GPIO.HIGH)
		GPIO.output(PWMA, GPIO.HIGH)
		GPIO.output(BIN1, GPIO.HIGH)
		GPIO.output(BIN2, GPIO.LOW)
		GPIO.output(PWMB, GPIO.HIGH)
		rightmotor.ChangeDutyCycle(30)
		leftmotor.ChangeDutyCycle(30)
		return WASDrightplace

	@cherrypy.expose
	def stop(self):
		GPIO.output(AIN1, GPIO.LOW)
		GPIO.output(AIN2, GPIO.HIGH)
		GPIO.output(PWMA, GPIO.LOW)
		GPIO.output(BIN1, GPIO.LOW)
		GPIO.output(BIN2, GPIO.HIGH)
		GPIO.output(PWMB, GPIO.LOW)
		rightmotor.ChangeDutyCycle(0)
		leftmotor.ChangeDutyCycle(0)
		return WASDrightplace
# program

rightmotor.start(0)
leftmotor.start(0)


cherrypy.server.socket_host = "0.0.0.0"  #0.0.0.0 =>  listen on all interfaces
cherrypy.quickstart(Christianscript())
