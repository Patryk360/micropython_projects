import sys
sys.path.append("/libs")
from machine import Pin
from time import sleep
import nrf24l01test

nrf24l01test.responder()