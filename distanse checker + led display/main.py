import sys
sys.path.append("/libs")
from machine import Pin, I2C
from pico_i2c_lcd import I2cLcd
from utime import sleep, sleep_us, ticks_us

i2c = I2C(0, sda=Pin(12), scl=Pin(13), freq=400000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

trig = Pin(15, Pin.OUT)
echo = Pin(14, Pin.IN)
led = Pin(25, Pin.OUT)

fps = 10

def distanse():
    trig.value(0)
    sleep_us(2)
    
    trig.value(1)
    sleep_us(5)
    trig.value(0)
    while echo.value() == 0:
        signaloff = ticks_us()

    while echo.value() == 1:
        signalon = ticks_us()
    
    timeresult = signalon - signaloff
    distanse = (((timeresult * (10 ** -6)) * 343.8 / 2)) * 100
    
    my_distanse = str(round(distanse, 2))
    lcd.clear()
    lcd.putstr("Dystans: \n"+my_distanse+" cm")
    sleep(1/fps)

while True:
    distanse()