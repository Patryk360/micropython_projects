from machine import UART, Pin, PWM
from time import sleep
import re

uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

led_front = Pin(4, Pin.OUT)
led_back = Pin(3, Pin.OUT)

servo = PWM(Pin(2))
servo.freq(50)

current_angle = 45

def set_angle(angle):
    global current_angle
    min_duty = 1638
    max_duty = 8192

    def angle_to_duty(a):
        return int(min_duty + (max_duty - min_duty) * a / 180)

    servo.duty_u16(angle_to_duty(angle))
    current_angle = angle

set_angle(45)

def split_l(s):
    result = []
    i = 0
    while i < len(s):
        if s[i].isalpha():
            start = i
            i += 1
            while i < len(s) and s[i].isdigit():
                i += 1
            result.append(s[start:i])
        else:
            i += 1
    return result

def rotate(percent, direction):
    if direction == "R":
        angle = int(45 - (percent * 45 / 100))
    elif direction == "L":
        angle = int(45 + (percent * 45 / 100))
    else:
        angle = 45
    print(angle)
    set_angle(angle)

lift = False

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

                print("RX:", line)

                if line == "X":
                    print("magnes on")
                if line == "x":
                    print("magnes off")
                if line == "W":
                    lift = True
                    print("lift on")
                if line == "w":
                    lift = False
                    print("lift off")
                if line == "U":
                    print("front lights on")
                if line == "u":
                    print("front lights off")
                if line == "V":
                    print("back lights on")
                if line == "v":
                    print("back lights off")
                    
                if not lift:
                    if line.startswith("F") or line.startswith("B"):
                        parts = split_l(line)
                        for part in parts:
                            if len(part) < 2:
                                continue
                            key = part[0]
                            val_str = part[1:]
                            if not val_str.isdigit():
                                continue
                            val = int(val_str)

                            if key == "F":
                                pass
                            elif key == "B":
                                pass
                            elif key == "R":
                                rotate(val, "R")
                            elif key == "L":
                                rotate(val, "L")
                else:
                    print("lift")

    sleep(0.1)