import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)

GPIO.setup(13, GPIO.OUT)

print "High"
GPIO.output(13, True)
time.sleep(2)
print "Low"
GPIO.output(13, False)

