from machine import Pin, ADC
from time import sleep
import ujson

leftJoyClick = Pin(33, Pin.IN, Pin.PULL_UP)
leftJoyX = ADC(Pin(32))
leftJoyX.atten(ADC.ATTN_11DB)
leftJoyX.width(ADC.WIDTH_12BIT)
leftJoyY = ADC(Pin(35))
leftJoyY.atten(ADC.ATTN_11DB)
leftJoyY.width(ADC.WIDTH_12BIT)

potentiometer = ADC(Pin(34))
potentiometer.atten(ADC.ATTN_11DB)
potentiometer.width(ADC.WIDTH_12BIT)

def joystick():
    percentageP = ((potentiometer.read_u16() / 65535) * 100)
    percentageX = ((leftJoyX.read_u16() / 65535) * 100)
    percentageY = ((leftJoyY.read_u16() / 65535) * 100)
    
    dataJSON = {
        "joystick": {
            "x": round(percentageX / 10) * 10,
            "y": round(percentageY / 10) * 10,
            "sw": leftJoyClick.value()
        },
        "motor": {
            "speed": round(percentageP / 5) * 5,
            "right": 0,
            "left": 1
        }
    }
    
    data = ujson.dumps(dataJSON)
    return data