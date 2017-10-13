import cherrypy
import RPi.GPIO as GPIO

file = open('/home/pi/htmlfile.html')
index_html = file.read()
file.close()

class Fuckmylife(object):
    @cherrypy.expose
    def index(self):
        return index_html

    @cherrypy.expose
    def on(self):
        GPIO.output(7, GPIO.HIGH)
        return index_html

    @cherrypy.expose
    def off(self):
        GPIO.output(7, GPIO.LOW)
        return index_html

    @cherrypy.expose
    def on2(self):
        GPIO.output(8, GPIO.HIGH)
        return index_html

    @cherrypy.expose
    def off(self):
        GPIO.output(8, GPIO.LOW)
        return index_html

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(7, GPIO.OUT)
GPIO.output(7, GPIO.HIGH)
GPIO.setup(8, GPIO.OUT)
GPIO.output(8, GPIO.HIGH)
cherrypy.server.socket_host = "0.0.0.0"  #0.0.0.0 =>  listen on all interfaces
cherrypy.quickstart(LEDController())
