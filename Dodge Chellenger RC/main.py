from machine import Pin, PWM
from time import sleep

pwm = PWM(Pin(32))
pwm.freq(50)

def set_angle(angle):
    min_ns = 600_000
    max_ns = 2400_000
    pulse = min_ns + (max_ns - min_ns) * angle / 180
    pwm.duty_ns(int(pulse))

def left(percent):
    percent = min(max(percent, 0), 100)
    angle = 90 - ((90 - 65) * percent / 100)
    set_angle(angle)

def right(percent):
    percent = min(max(percent, 0), 100)
    angle = 90 + ((110 - 90) * percent / 100)
    set_angle(angle)

speaker = PWM(Pin(25))

def beep(freq, duration):
    speaker.freq(freq)
    speaker.duty(20)
    sleep(duration)
    speaker.duty(0)

#beep(500, 0.5)

power = 700

RPWM = Pin(27, Pin.OUT)
LPWM = Pin(13, Pin.OUT)

R_EN = PWM(Pin(26))
R_EN.freq(20000)
L_EN = PWM(Pin(12))
L_EN.freq(20000)

RPWM.on()
LPWM.off()

left(100)

R_EN.duty(power)
L_EN.duty(power)