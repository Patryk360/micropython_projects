from machine import Pin, ADC, PWM, SoftI2C
from ssd1306 import SSD1306_I2C
from time import sleep
import config
sensor_1 = ADC(Pin(0))
sensor_2 = ADC(Pin(1))

i2c = SoftI2C(scl=Pin(9), sda=Pin(8))
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

en_1 = PWM(Pin(21))
en_1.freq(20000)
en_1_in_1 = Pin(3, Pin.OUT)
en_1_in_2 = Pin(2, Pin.OUT)
en_1_in_1.value(1)
en_1_in_2.value(0)

en_2 = PWM(Pin(20))
en_2.freq(20000)
en_2_in_3 = Pin(5, Pin.OUT)
en_2_in_4 = Pin(6, Pin.OUT)
en_2_in_3.value(0)
en_2_in_4.value(1)

def start():
    print("AUTO")
    while True:
        if (sensor_1.read_u16() < 50000):
            en_1.duty_u16(0)
        else:
            en_1.duty_u16(65535)
            
        if (sensor_2.read_u16() < 50000):
            en_2.duty_u16(0)
        else:
            en_2.duty_u16(65535)
        
        oled.fill(0)
        oled.text("ADC L: "+str(sensor_1.read_u16()), 0, 0)
        oled.text("ADC R: "+str(sensor_2.read_u16()), 0, 10)
        oled.text("PWM L: "+str(en_1.duty_u16()), 0, 30)
        oled.text("PWM R: "+str(en_2.duty_u16()), 0, 40)
        oled.show()
        
        sleep(0.1)
