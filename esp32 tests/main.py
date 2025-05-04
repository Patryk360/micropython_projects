import sys
sys.path.append("/libs")

from machine import Pin, ADC, PWM, I2C
from ssd1306 import SSD1306_I2C
from ADS1115 import *
from time import sleep

mq6 = ADC(Pin(0))
mq6.atten(ADC.ATTN_11DB)

i2c = I2C(scl=Pin(9), sda=Pin(8))
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

adc = ADS1115(i2c=i2c)

def read_mq6():
    raw_value = mq6.read_u16()
    voltage = raw_value / 65535 * 3.3
    return voltage

adc.setVoltageRange_mV(ADS1115_RANGE_4096)

def read(channel):
    adc.setCompareChannels(channel)
    adc.startSingleMeasurement()
    while adc.isBusy():
        pass
    res = adc.getRawResult()
    return res

while True:
        alcohol_voltage = read_mq6()
        oled.fill(0)
        oled.text("V: "+str(round(alcohol_voltage, 2)), 0, 0)
        oled.text("ADC ESP32: "+str(mq6.read_u16()), 0, 10)
        oled.text("ADC 0: "+str(read(ADS1115_COMP_0_GND)), 0, 20)
        oled.text("ADC 1: "+str(read(ADS1115_COMP_1_GND)), 0, 30)
        oled.show()