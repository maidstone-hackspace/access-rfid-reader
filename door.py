import RPi.GPIO as GPIO
import time

pwmPin = 18

duty = 100

GPIO.setmode(GPIO.BCM)
#GPIO.setup(pwmPin,GPIO.OUT)

def setup(pwnPin=18):
    GPIO.setup(pwmPin, GPIO.OUT)

def unlock_door(pwmPin=18, delay=3):
    GPIO.output(pwmPin,GPIO.HIGH)
    time.sleep(delay)
    GPIO.output(pwmPin,GPIO.LOW)


if __name__ == "__main__":
    try:
       while 1:
           unlock_door()
           time.sleep(3)

    except KeyboardInterrupt:
        GPIO.cleanup()
