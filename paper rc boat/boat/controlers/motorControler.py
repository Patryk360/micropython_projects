from machine import Pin, PWM
from time import sleep

def scalePWM(value):
    if value < 0:
        value = 0
    elif value > 255:
        value = 255
    return int(value * 65535 / 255)

def motorSpeed(speed):
    pwm_motor = PWM(15)
    pwm_motor.duty_u16(scalePWM((255 * speed) / 100))
    pwm_motor.freq(7000)

motor_l = Pin(20, Pin.OUT)
motor_r = Pin(21, Pin.OUT)

def motorLeft():
    motor_l.value(1)
    motor_r.value(0)

def motorRight():
    motor_l.value(0)
    motor_r.value(1)

def motorStop():
    motor_l.value(0)
    motor_r.value(0)