import time
import serial
import RPi.GPIO as GPIO


from contextlib import contextmanager

sp = "/dev/serial0"


@contextmanager
def nfc(*args, **kwds):
    print(args)
    print(kwds)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.OUT)
    GPIO.output(23, False)
    GPIO.output(24, False)
    serial_port = serial.Serial(sp, 9600)

    try:
        yield serial_port
    finally:
        serial_port.close()


def read_code(port):
    print("read_code")
    ID = b""
    read_byte = port.read()
    if read_byte == b"\x02":
        for Counter in range(12):
            read_byte = port.read()
            ID += read_byte
        # print(str(ID))
        return ID
    return None


# PortRF = serial.Serial('/dev/ttyS0',9600)
if __name__ == "__main__":
    with nfc(sp) as PortRF:
        while True:
            code = read_code(PortRF)
            print("The code for this card is %s" % str(code))
