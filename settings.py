import os
from dotenv import load_dotenv
load_dotenv()

PORT = "/dev/serial0"

DEVICE_ID = os.getenv('DEVICE_ID')
SECRET = os.getenv('SECRET')

MATRIX_USER = os.getenv('MATRIX_USERNAME')
MATRIX_PASSWORD = os.getenv('MATRIX_PASSWORD')
MATRIX_ROOM = os.getenv('MATRIX_ROOM')
