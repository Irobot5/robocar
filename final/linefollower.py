#1 1 1  forward (in the crossroads)
#0 0 0  turn around to find a line

#1 0 0  turn left (back to line)
#0 1 0  forward
#0 0 1  turn right (back to line)

#1 1 0  turn left (on the corner, with 90 degrees)
#1 0 1  ???
#0 1 1  turn right (ont the corner, with 90 degrees)

import signal, os
import RPi.GPIO as GPIO
import time

AIN1 = 2
AIN2 = 3
PWMA = 17
BIN1 = 22
BIN2 = 18
PWMB = 27


# Pin Definitons:
IRsensor1 = 5       #mid
IRsensor2 = 4     #left
IRsensor3 = 6     #right


# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(IRsensor1, GPIO.IN) # sensor set as input
GPIO.setup(IRsensor2, GPIO.IN)
GPIO.setup(IRsensor3, GPIO.IN)
GPIO.setwarnings(False)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)


# variables
rightmotor = GPIO.PWM(PWMA, 50)
leftmotor = GPIO.PWM(PWMB, 50)

def handler(signum, frame):  #stop when ctrl-c is recieved
    print ('Signal handler called with signal', signum)
    print ('exiting')
    GPIO.output(PWMA, GPIO.LOW)
    GPIO.output(PWMB, GPIO.LOW)
    GPIO.cleanup()
    exit(0)

# When recieving ctrl-C
signal.signal(signal.SIGINT, handler)

def forward():
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
    rightmotor.start(0)
    leftmotor.start(0)
    rightmotor.ChangeDutyCycle(60)
    leftmotor.ChangeDutyCycle(60)

def back():
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)
    rightmotor.start(0)
    leftmotor.start(0)
    rightmotor.ChangeDutyCycle(40)
    leftmotor.ChangeDutyCycle(40)

def stop():
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
    rightmotor.start(0)
    leftmotor.start(0)
    rightmotor.ChangeDutyCycle(0)
    leftmotor.ChangeDutyCycle(0)

def leftabit():
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
    rightmotor.start(0)
    leftmotor.start(0)
    rightmotor.ChangeDutyCycle(35)
    leftmotor.ChangeDutyCycle(10)

def rightabit():
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
    rightmotor.start(0)
    leftmotor.start(0)
    rightmotor.start(10)
    leftmotor.start(35)

def shouldgocheck(A, B, C):
    if A==1 and B==1 and C==1:
        shouldgo="forward"
    elif A==1 and B==0 and C==0:
        shouldgo="right"
    elif A==0 and B==1 and C==0:
        shouldgo="forward"
    elif A==0 and B==0 and C==1:
        shouldgo="left"
    elif A==1 and B==1 and C==0:
        shouldgo="right"
    elif A==1 and B==0 and C==1:
        shouldgo="forward"
    elif A==0 and B==1 and C==1:
        shouldgo="left"
    elif A==0 and B==0 and C==0:
        shouldgo="backward"
    else:
        print("cannot find the direction and the last one is: " ,shouldgo)
    return shouldgo

def realdirection(shouldgo):
    if shouldgo=="forward":
        forward()
    elif shouldgo=="left":
        leftabit()
    elif shouldgo=="right":
        rightabit()
    elif shouldgo=="stop":
        stop()
    elif shouldgo=="backward":
        back()
    else:
        print("shouldgo has an invaild value")

#run


shouldgo="w"
while True:
    A = GPIO.input(IRsensor2)
    B = GPIO.input(IRsensor1)
    C = GPIO.input(IRsensor3)
    realdirection(shouldgocheck(A, B, C))
    signal.signal(signal.SIGINT, handler)
    print(A, B, C)
    time.sleep(0.01)




