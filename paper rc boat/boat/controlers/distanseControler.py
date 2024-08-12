from machine import Pin
from utime import sleep_us, ticks_us
trig = Pin(8, Pin.OUT)
echo = Pin(7, Pin.IN)

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
    
    my_distanse = round(distanse, 2)
    return my_distanse