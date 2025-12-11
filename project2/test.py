from machine import Pin, PWM
from time import sleep

in1 = PWM(Pin(3))
in1.freq(5000)
in1.duty_u16(40000)
in2 = PWM(Pin(4))
in2.freq(5000)
in2.duty_u16(40000)

in1.duty(1000)
in2.duty(0)
sleep(10)
in1.duty(0)
in2.duty(500)