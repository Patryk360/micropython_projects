from machine import Pin, ADC
from time import sleep

leftJoyClick = Pin(33, Pin.IN, Pin.PULL_UP)
leftJoyX = ADC(Pin(32))
leftJoyX.atten(ADC.ATTN_11DB)
leftJoyX.width(ADC.WIDTH_12BIT)
leftJoyY = ADC(Pin(35))
leftJoyY.atten(ADC.ATTN_11DB)
leftJoyY.width(ADC.WIDTH_12BIT)

test = ADC(Pin(34))
test.atten(ADC.ATTN_11DB)
test.width(ADC.WIDTH_12BIT)

def joystick():
    print(leftJoyX.read_u16())
    print(leftJoyY.read_u16())
    print("SW: " + str(leftJoyClick.value()))
    percentage = ((test.read_u16() / 65535) * 100)
    print("P: " + str(round(percentage / 10) * 10))