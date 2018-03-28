import RPi.GPIO as gpio
import time
import datetime
import jwt
import requests
import nfc
import logging


gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
#rfid
gpio.setup(17,gpio.OUT)

#strike
gpio.setup(18,gpio.OUT)


DEVICE_ID = '62ef7d94-4c56-41ba-8694-550e4b0ef5e9'
SECRET = 'kjlsdlkdskldf'
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
#logging.basicConfig(filename='/tmp/rfid.log', level=logging.DEBUG)

def trigger_door(mode=False):
    if mode is True:
       print('door activate')
       gpio.output(18,gpio.HIGH)
    time.sleep(1)
    gpio.output(18,gpio.LOW)

def flash_led(mode=False):
    if mode is True:
        gpio.output(17,gpio.HIGH)
        time.sleep(1)
        gpio.output(17,gpio.LOW)
    if mode is False:
        for _ in range(0, 3):
            gpio.output(17, gpio.HIGH)
            time.sleep(0.1)
            gpio.output(17, gpio.LOW)
            time.sleep(0.1)
    time.sleep(1)

def open():
    trigger_door(True)
    flash_led('on')
    logging.info('Request allowed')
    pass


def deny():
    trigger_door(True)
    logging.info('Request denied')
    pass


def check_valid(rfid_token):
    encoded = jwt.encode({
        'rfid_code': rfid_token,
        'device_id': DEVICE_ID,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=2)
    }, SECRET, algorithm='HS256')

    # response = requests.post('https://maidstone-hackspace.org.uk/rfid', data=encoded)
    body = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdXRoZW50aWNhdGVkIjp0cnVlLCJleHAiOjE1MTgwMzA0ODR9.gmarIZPt8HML1WzHqmlau5E9o0FyrMuS_pxlo3vfOuw'

    thing = jwt.decode(body, SECRET, algorithms=['HS256'])

    if thing['authenticated'] is True:
        open()
    else:
        deny()


while True:
    logging.info('RFID Reader started')
    with nfc.ContactlessFrontend('tty:S0:pn532') as clf:
        logging.debug('Listening on %s' % clf)
        tag = clf.connect(rdwr={'on-connect': lambda tag: False})
        code = str(tag.identifier).encode('hex')
        logging.info('Detected RFID card %s' % code)
        try:
            check_valid(code)
            flash_led(True)
        except Exception as e:
            logging.exception(e)
            flash_led(False)
            deny()
