import datetime
import jwt
import requests
#import nfc
import os
import logging
import nfc_rdm6300 as nfc
from time import sleep
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(filename='/tmp/rfid.log', level=logging.DEBUG)


def allow():
    logging.info('Request allowed')
    pass


def deny():
    logging.info('Request denied')
    pass


def check_valid(rfid_token):
    if not rfid_token:
        return
    encoded = jwt.encode({
        'rfid_code': rfid_token.decode("utf-8"),
        'device_id': os.getenv('DEVICE_ID'),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=2)
    }, os.getenv('SECRET'), algorithm='HS256')
    logging.debug("Sending request with data: %s" % encoded)
    response = requests.post(os.getenv('URL', 'https://maidstone-hackspace.org.uk/api/v1/rfid_auth/'), data={"data":encoded}, timeout=3)
    if response.status_code != 200:
        logging.info("Response code not valid")
        return deny()
    logging.debug("Response body: %s" % response.json())
    parsed_response = jwt.decode(response.json(), os.getenv('SECRET'), algorithms=['HS256'], verify=False)

    if parsed_response['authenticated'] is True:
        logging.info("User %s has been authenticated" % parsed_response['username'])
        allow()
    else:
        deny()

clf = "/dev/ttyS0"
with nfc.nfc("/dev/ttyS0") as port:
    logging.info('RFID Reader started')
    while True:
    #with nfc.ContactlessFrontend('tty:S0:pn532') as clf:
        logging.debug('Listening on %s' % clf)
        #tag = clf.connect(rdwr={'on-connect': lambda tag: False})
        #code = str(tag.identifier).encode('hex')
        code = nfc.read_code(port)

        logging.info('Detected RFID card %s' % code)
        try:
            check_valid(code)
        except Exception as e:
            logging.exception(e)
            deny()
        sleep(0.1)
