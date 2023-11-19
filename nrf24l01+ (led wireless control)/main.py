import sys
sys.path.append("/libs")
from nrf24l01 import NRF24L01
from machine import SPI, Pin
from time import sleep

import nrf24l01test

led = Pin(25, Pin.OUT)

led.value(1)
sleep(3)
led.value(0)

nrf24l01test.slave()