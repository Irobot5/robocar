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
leftmotor = GPIO.PWM(PWMA, 50)
rightmotor = GPIO.PWM(PWMB, 50)

def handler(signum, frame):  #stop when ctrl-c is recieved
    print 'Signal handler called with signal', signum
    print 'exiting'
    GPIO.output(PWMA, GPIO.LOW)
    GPIO.output(PWMB, GPIO.LOW)
    GPIO.cleanup()
    exit(0)

# When recieving ctrl-C
signal.signal(signal.SIGINT, handler)

def main():
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(PWMA, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
    GPIO.output(PWMB, GPIO.HIGH)


def stop():
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(PWMA, GPIO.LOW)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
    GPIO.output(PWMB, GPIO.LOW)

try:
    while True:
        A = GPIO.input(IRsensor2)
        B = GPIO.input(IRsensor1)
        C = GPIO.input(IRsensor3)
        if not (not (A == 1 and B == 1 and C == 1) and not (A == 0 and B == 1 and C == 0) and not (
                    A == 1 and B == 0 and C == 1)):
            main()
            rightmotor.start(50)
            leftmotor.start(50)
            time.sleep(0.05)
        elif A==0 and B==1 and C==1:
            main()
            rightmotor.start(25)
            leftmotor.start(45)
            time.sleep(0.05)
        elif A==0 and B==0 and C==1:
            main()
            rightmotor.start(0)
            leftmotor.start(45)
            time.sleep(0.05)
        elif A==1 and B==1 and C==0:
            main()
            rightmotor.start(45)
            leftmotor.start(25)
            time.sleep(0.05)
        elif A==1 and B==0 and C==0:
            main()
            rightmotor.start(45)
            leftmotor.start(0)
            time.sleep(0.05)
        else:
            print("panic!!")
        signal.signal(signal.SIGINT, handler)
        print(A,B,C)
except:
    print("MRKLKRLRKR")