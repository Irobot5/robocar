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

#assigning H-bridge pins to GPIO
AIN1 = 2 #leftmotor negative
AIN2 = 3 #leftmotor positive
PWMA = 17 #leftmotor on/off
BIN1 = 22 #rightmotor negative
BIN2 = 18 #rightmotor positive
PWMB = 27 #rightmotor on/off


#line reader sensor Pin Definitons:
IRsensor1 = 5       #mid
IRsensor2 = 4     #left
IRsensor3 = 6     #right

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(IRsensor1, GPIO.IN) # sensor set as input
GPIO.setup(IRsensor2, GPIO.IN)
GPIO.setup(IRsensor3, GPIO.IN)
GPIO.setwarnings(False)#disabling warnings for constant running
GPIO.setup(AIN1, GPIO.OUT)#assigning H-bridge pins to output
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(BIN1, GPIO.OUT)
GPIO.setup(BIN2, GPIO.OUT)
GPIO.setup(PWMB, GPIO.OUT)

#assinging motor variables
leftmotor = GPIO.PWM(PWMA, 50) #frequency and what the motor pin is
rightmotor = GPIO.PWM(PWMB, 50)

def handler(signum, frame):  #stop when ctrl-c is recieved or else you die
    print 'Signal handler called with signal', signum
    print 'exiting'
    GPIO.output(PWMA, GPIO.LOW)#turning off the motor or else the car would be left on and keep driving after exit
    GPIO.output(PWMB, GPIO.LOW)
    GPIO.cleanup()#simple cleanup setting all pins back to original state(input)
    exit(0)#exits the program

# When recieving ctrl-C
signal.signal(signal.SIGINT, handler)#calls the command plus adding it into the loop so not to crash
#defining every direction
def forward():
    GPIO.output(AIN1, GPIO.LOW)#low on AIN/BIN 1 and high on 2 to go forward and opposite to go backwards
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(PWMA, GPIO.HIGH)#PWM set to high for start if LOW it will not run
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
    GPIO.output(PWMB, GPIO.HIGH)
    rightmotor.ChangeDutyCycle(30)#setting the speed of the car at 30% of 5volt.
    leftmotor.ChangeDutyCycle(30)


def backward():
    GPIO.output(AIN1, GPIO.HIGH)#when going backwards the settings will be the opposite of the forward def
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(PWMA, GPIO.HIGH)#the PWM is only there to keep the motor on and off, so we will still have it as high for on
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)
    GPIO.output(PWMB, GPIO.HIGH)
    rightmotor.ChangeDutyCycle(20)#still speed
    leftmotor.ChangeDutyCycle(20)


def rightward():
    GPIO.output(AIN1, GPIO.LOW)#when turning the princible is changed
    GPIO.output(AIN2, GPIO.HIGH)#the AIN will have to go forward
    GPIO.output(PWMA, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.LOW)#the BIN will be off for a hard right turn
    GPIO.output(PWMB, GPIO.HIGH)
    rightmotor.ChangeDutyCycle(30)#still speed
    leftmotor.ChangeDutyCycle(30)


def leftward():
    GPIO.output(AIN1, GPIO.LOW)#the opposite again is used for left
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(PWMA, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
    GPIO.output(PWMB, GPIO.HIGH)
    rightmotor.ChangeDutyCycle(30)
    leftmotor.ChangeDutyCycle(30)


def stop():
    GPIO.output(PWMA, GPIO.LOW)#stopping the car is simply done by turning off the PWM for both motors
    GPIO.output(PWMB, GPIO.LOW)
    #speed is not necessary here

def leftabit():
    GPIO.output(AIN1, GPIO.LOW)#the same as forward
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(PWMA, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
    GPIO.output(PWMB, GPIO.HIGH)
    rightmotor.ChangeDutyCycle(20)#speed is different for a smaller adjustment in direction
    leftmotor.ChangeDutyCycle(5)#a lower speed

def rightabit():
    GPIO.output(AIN1, GPIO.LOW)#same as leftabit
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(PWMA, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
    GPIO.output(PWMB, GPIO.HIGH)
    rightmotor.ChangeDutyCycle(5)#but with the speed opposite for the motors
    leftmotor.ChangeDutyCycle(20)
#we used to different ways to define a turn, a full turn and a small turn one only using one motor and one using both motors

def shouldgocheck(A, B, C): #defining the input and direction
    if A==1 and B==1 and C==1: #when given and input fromt the sensor it will create or change a variable with the word for the corrosponding given number.
        shouldgo="forward" #so when given input 111 the car should go forward
    elif A==1 and B==0 and C==0:
        shouldgo="left" #and when given 100 it should go left
    elif A==0 and B==1 and C==0:
        shouldgo="forward" #if then recieving only 1 its should still go forward sinc eits still on path
    elif A==0 and B==0 and C==1:
        shouldgo="right"
    elif A==1 and B==1 and C==0:
        shouldgo="leftabit"
    elif A==1 and B==0 and C==1:
        shouldgo="forward"
    elif A==0 and B==1 and C==1:
        shouldgo="rightabit"
    elif A==0 and B==0 and C==0:
        shouldgo="back"
    else:
        print("cannot find the direction and the last one is: " ,shouldgo)#if nothing is given it should display the text and run again, so it wont quit the program because of a fault.
    return shouldgo#returning the result of the defintion to the program

def realdirection(shouldgo):
    if shouldgo=="forward":
        forward() #when forward is given the definition forward is used
    elif shouldgo=="left":
        leftward()#when left is given the definition leftward is used
    elif shouldgo=="right":
        rightward()
    elif shouldgo=="leftabit":
        leftabit()#when at close ot the edge go a tiny bit to the other side
    elif shouldgo=="rightabit":
        rightabit()
    elif shouldgo=="back":
        backward()
    else:
        print("shouldgo has an invaild value")#a message to show something went wrong

#run

rightmotor.start(0)#giving the motor a start input after setup
leftmotor.start(0)

while True:
    A = GPIO.input(IRsensor2)
    B = GPIO.input(IRsensor1)
    C = GPIO.input(IRsensor3)
    realdirection(shouldgocheck(A, B, C))
    signal.signal(signal.SIGINT, handler)
    print(A, B, C)
    time.sleep(0.01)

#hi2
