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


#sound sensor Pin Definitons:
triggerpina = #a is front sensor
triggerpinb = #b is back sensor
echopina =
echopinb =
IRsensor1 = 5       #mid
IRsensor2 = 4     #left
IRsensor3 = 6     #right

# Pin Setup:
GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
GPIO.setup(triggerpina,GPIO.OUT)
GPIO.setup(triggerpinb,GPIO.OUT)
GPIO.setup(echopina,GPIO.IN)
GPIO.setup(echopinb,GPIO.IN)
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

def reading(sensor):
    pingtime = 0
    echotime = 0
    if sensor == 0:
        GPIO.output(13,GPIO.LOW)
        GPIO.output(13,GPIO.HIGH)
        pingtime=time.time()
        time.sleep(0.00001)
        GPIO.output(13,GPIO.LOW)
        while GPIO.input(19)==0:
            pingtime = time.time()
        while GPIO.input(19)==1:
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
def shouldgocheck(A, B, C): #defining the input and direction
    if A==1 and B==1 and C==1: #when given and input fromt the sensor it will create or change a variable with the word for the corrosponding given number.
        shouldgo="backward"
    else:
         print("im fine bra")
	return shouldgo
def realdirection(shouldgo):
    if shouldgo=="backward":
        backward()
        time.sleep(1)
	else:
        print("mrklmerk")
while True:
    A = GPIO.input(IRsensor2)
    B = GPIO.input(IRsensor1)
    C = GPIO.input(IRsensor3)
    realdirection(shouldgocheck(A, B, C))
    signal.signal(signal.SIGINT, handler)
    print(A, B, C)
    time.sleep(0.01)

