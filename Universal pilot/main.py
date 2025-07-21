import sys
sys.path.append("/libs")
sys.path.append("/modes")

from time import sleep
from machine import Pin, I2C, ADC
import linefollower
import boat
import chellenger
from ssd1306 import SSD1306_I2C
from ADS1115 import *

i2c = I2C(scl=Pin(9), sda=Pin(8))
adc = ADS1115(i2c=i2c)
adc.setVoltageRange_mV(ADS1115_RANGE_4096)
oled = SSD1306_I2C(128, 64, i2c)

sw_right = Pin(3, Pin.IN, Pin.PULL_UP)
sw_left = Pin(2, Pin.IN, Pin.PULL_UP)

def read(channel):
    adc.setCompareChannels(channel)
    adc.startSingleMeasurement()
    while adc.isBusy():
        pass
    res = adc.getRawResult()
    return res

mode = 0
modes = ["linefollower", "boat", "chellenger", "test2", "test3"]

pot = ADC(Pin(0))

while True:
    if read(ADS1115_COMP_1_GND) < 8000:
        if mode < 4:
            mode += 1
            print("down")
    if read(ADS1115_COMP_1_GND) > 20000:
        if mode > 0:
            mode -= 1
            print("up")
    
    oled.fill(0)
    oled.text(f"{mode+1}. {modes[mode]}", 0, 0)
    oled.show()
    if sw_right.value() == 0:
        if mode == 0:
            linefollower.start()
            sleep(2)
        if mode == 1:
            boat.start()
            sleep(2)
        if mode == 2:
            chellenger.start()
            sleep(2)
    sleep(0.15)