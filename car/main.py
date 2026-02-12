from machine import UART, Pin, PWM
from time import sleep
import re

# BT
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

# Lights
led_front = Pin(2, Pin.OUT, value=0, pull=Pin.PULL_DOWN)
led_back = Pin(3, Pin.OUT, value=0, pull=Pin.PULL_DOWN)

# Steering servo_1
servo_1 = PWM(Pin(4))
servo_1.freq(50)
current_angle = 45

def set_servo_1_angle_1(angle):
    global current_angle
    min_duty = 1966
    max_duty = 7864

    def angle_to_duty(a):
        return int(min_duty + (max_duty - min_duty) * a / 180)

    servo_1.duty_u16(angle_to_duty(angle))
    current_angle = angle

set_servo_1_angle_1(45)

# Engine Drive
in1 = Pin(8, Pin.OUT, value=0, pull=Pin.PULL_DOWN)
in2 = Pin(9, Pin.OUT, value=0, pull=Pin.PULL_DOWN)
    
pwm_engine = PWM(Pin(10))
pwm_engine.freq(10000)
pwm_engine.duty_u16(0)

def set_engine_drive(direction, speed_val):
    """
    direction: 0 dla przodu, 1 dla tyłu
    speed_val: wartość 0-65535
    """
    pwm_engine.duty_u16(speed_val)
    if direction == 0:
        in1.value(1)
        in2.value(0)
    else:
        in1.value(0)
        in2.value(1)

def parse_commands(command_string):
    """Rozdziela ciągi znaków na literę i wartość (np. F100R50)"""
    result = []
    i = 0
    while i < len(command_string):
        if command_string[i].isalpha():
            start = i
            i += 1
            while i < len(command_string) and command_string[i].isdigit():
                i += 1
            result.append(command_string[start:i])
        else:
            i += 1
    return result

def set_steering(percent, direction_key):
    """Oblicza kąt serwa na podstawie procentu skrętu"""
    if direction_key == "R":
        angle = int(45 - (percent * 45 / 100))
    elif direction_key == "L":
        angle = int(45 + (percent * 45 / 100))
    else:
        angle = 45
    set_servo_1_angle_1(angle)

# Status variables
is_lift_active = False
buffer = ""

while True:
    if uart.any():
        data = uart.read()
        if data:
            try:
                buffer += data.decode('utf-8')
            except UnicodeError:
                pass

            while '\n' in buffer:
                line, buffer = buffer.split('\n', 1)
                line = line.strip()
                if not line:
                    continue

                print("Otrzymano:", line)

                # Komendy proste
                if line == "X": print("Magnes: ON")
                if line == "x": print("Magnes: OFF")
                if line == "W": 
                    is_lift_active = True
                    print("Blokada LIFT: ON")
                if line == "w": 
                    is_lift_active = False
                    print("Blokada LIFT: OFF")
                
                # Światła
                if line == "U": led_front.value(1)
                if line == "u": led_front.value(0)
                if line == "V": led_back.value(1)
                if line == "v": led_back.value(0)
                    
                # Sterowanie jazdą
                if not is_lift_active:
                    if line.startswith("F") or line.startswith("B"):
                        command_parts = parse_commands(line)
                        for part in command_parts:
                            if len(part) < 2:
                                continue
                            
                            key = part[0]
                            val_str = part[1:]
                            if not val_str.isdigit():
                                continue
                            
                            val = int(val_str)

                            if key == "F":
                                set_engine_drive(1, int(60000 * (val / 100)))
                            elif key == "B":
                                set_engine_drive(0, int(60000 * (val / 100)))
                            elif key == "R":
                                set_steering(val, "R")
                            elif key == "L":
                                set_steering(val, "L")
                else:
                    print("Pojazd w trybie LIFT")

    sleep(0.01)