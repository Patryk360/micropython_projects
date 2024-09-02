import sys
sys.path.append("/libs")
from machine import Pin, SoftI2C
from time import sleep
import nrf24l01test
from ssd1306 import SSD1306_I2C

i2c = SoftI2C(scl=Pin(9), sda=Pin(8))
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

oled.text('Hello, World!', 0, 0)
oled.show()

sleep(3)
oled.fill(0)
oled.text('On!', 0, 0)
oled.show()

nrf24l01test.initiator()