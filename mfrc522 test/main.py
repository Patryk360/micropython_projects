import sys
sys.path.append("/libs")

from machine import Pin, SoftSPI
from time import sleep_ms
from mfrc522 import MFRC522

sck = Pin(8, Pin.OUT)
mosi = Pin(10, Pin.OUT)
miso = Pin(9, Pin.OUT)
spi = SoftSPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)

sda = Pin(6, Pin.OUT)

while True:
    rdr = MFRC522(spi, sda)
    uid = ""
    (stat1, tag_type) = rdr.request(rdr.REQIDL)
    if stat1 == rdr.OK:
        (stat2, raw_uid) = rdr.anticoll()
        if stat2 == rdr.OK:
            uid = ("0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
            print(uid)
            sleep_ms(100)