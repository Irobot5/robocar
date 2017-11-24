import signal, os
import RPi.GPIO as GPIO
import time#this is time

#assigning H-bridge pins to GPIO
AIN1 = 2 #leftmotor negative
AIN2 = 3 #leftmotor positive
PWMA = 17 #leftmotor on/off
BIN1 = 22 #rightmotor negative
BIN2 = 18 #rightmotor positive
PWMB = 27 #rightmotor on/off


#sound sensor Pin Definitons:
triggerpin = 13#a is front sensor
echopin = 19
IRsensor1 = 5       #mid
IRsensor2 = 4     #left
IRsensor3 = 6     #right

A = GPIO.input(IRsensor2)
B = GPIO.input(IRsensor1)
C = GPIO.input(IRsensor3)

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(triggerpina,GPIO.OUT)
GPIO.setup(echopina,GPIO.IN)
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
    GPIO.output(AIN1, GPIO.LOW)
    GPIO.output(AIN2, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
    rightmotor.start(0)
    rightmotor.start(0)
    rightmotor.ChangeDutyCycle(80)
    leftmotor.ChangeDutyCycle(80)


def backward():
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(BIN1, GPIO.HIGH)
    GPIO.output(BIN2, GPIO.LOW)
    rightmotor.start(0)
    leftmotor.start(0)
    rightmotor.ChangeDutyCycle(80)
    leftmotor.ChangeDutyCycle(80)


def leftward():
    GPIO.output(AIN1, GPIO.HIGH)
    GPIO.output(AIN2, GPIO.LOW)
    GPIO.output(PWMA, GPIO.HIGH)
    GPIO.output(BIN1, GPIO.LOW)
    GPIO.output(BIN2, GPIO.HIGH)
    GPIO.output(PWMB, GPIO.HIGH)
    rightmotor.start(0)
    leftmotor.start(0)
    rightmotor.ChangeDutyCycle(20)
    leftmotor.ChangeDutyCycle(20)

#we used to different ways to define a turn, a full turn and a small turn one only using one motor and one using both motors

def reading(sensor):
    pingtime = 0
    echotime = 0
    if sensor == 0:
        GPIO.output(triggerpin,GPIO.LOW)
        GPIO.output(triggerpin,GPIO.HIGH)
        pingtime=time.time()
        time.sleep(0.00001)
        GPIO.output(triggerpin,GPIO.LOW)
        while GPIO.input(echopin)==0:
            pingtime = time.time()
        while GPIO.input(echopin)==1:
            echotime=time.time()
        if (echotime is not None) and (pingtime is not None):
            elapsedtime = echotime - pingtime
            distance = elapsedtime * 17000
        else:
            distance = 0
        print(pingtime)
        print(echotime)
        return distance
"""if distance is closer than 150 cm then the car shuld mov forward
the should not driver over any black lines"""


while True:
    realdistence = reading(0)
    signal.signal(signal.SIGINT, handler)
    print(realdistence)
    print(A, B, C)
    if A == 1 or B == 1 or C == 1:
        for hk in range(0, 100):
            hk= hk+1
            backward()
    else:
        if realdistence < 100:
            forward()
        else:
            leftward()
    time.sleep(0.01)
