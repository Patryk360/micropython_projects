from machine import Pin, ADC, PWM, SoftI2C
from ssd1306 import SSD1306_I2C
from time import sleep

sensor_left = ADC(Pin(0))
sensor_left.atten(ADC.ATTN_11DB)
sensor_right = ADC(Pin(1))
sensor_right.atten(ADC.ATTN_11DB)

i2c = SoftI2C(scl=Pin(9), sda=Pin(8))
oled = SSD1306_I2C(128, 64, i2c)

# Silniki
pwm_left = PWM(Pin(4))
pwm_left.freq(20000)
in1_left = Pin(21, Pin.OUT)
in2_left = Pin(20, Pin.OUT)
in1_left.on()
in2_left.off()

pwm_right = PWM(Pin(3))
pwm_right.freq(20000)
in3_right = Pin(6, Pin.OUT)
in4_right = Pin(5, Pin.OUT)
in3_right.on()
in4_right.off()

# Zakres prędkości
min_speed = 43000
max_speed = 65000

def engine(percent):
    value = min_speed + (max_speed - min_speed) * (percent / 100)
    return int(value)

def reset():
    in1_left.on()
    in2_left.off()
    in3_right.on()
    in4_right.off()

def turn_left():
    in1_left.off()
    in2_left.on()
    pwm_left.duty_u16(engine(100))
    in3_right.on()
    in4_right.off()
    pwm_right.duty_u16(engine(100))

def turn_right():
    in1_left.on()
    in2_left.off()
    pwm_left.duty_u16(engine(100))
    in3_right.off()
    in4_right.on()
    pwm_right.duty_u16(engine(100))

def start():
    while True:
        if sensor_left.read() > 1000 and sensor_right.read() > 1000:
            reset()
            pwm_left.duty_u16(engine(50))
            pwm_right.duty_u16(engine(50))
        else:
            if sensor_left.read() < 1000:
                turn_left()
            if sensor_right.read() > 1000:
                turn_right()
                
        oled.fill(0)
        oled.text(f"S L:{sensor_left.read()}", 0, 0)
        oled.text(f"S R:{sensor_right.read()}", 0, 10)
        oled.show()