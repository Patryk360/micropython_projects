from machine import Pin, PWM, SoftI2C
from ssd1306 import SSD1306_I2C
import network
import socket
import ujson
import config
from time import sleep
import config

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
    value = int(min_speed + (max_speed - min_speed) * (percent / 100))
    return value

def back():
    in1_left.off()
    in2_left.on()
    in3_right.off()
    in4_right.on()

def reset():
    in1_left.on()
    in2_left.off()
    in3_right.on()
    in4_right.off()

def turn_left(percent):
    in1_left.off()
    in2_left.on()
    pwm_left.duty_u16(engine(percent))
    in3_right.on()
    in4_right.off()
    pwm_right.duty_u16(engine(percent))

def turn_right(percent):
    in1_left.on()
    in2_left.off()
    pwm_left.duty_u16(engine(percent))
    in3_right.off()
    in4_right.on()
    pwm_right.duty_u16(engine(percent))

def start():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(ssid=config.ssid, password=config.password, authmode=3, channel=11)

    print("AP active!")
    print("IP:", ap.ifconfig()[0])

    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]

    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print("Server running on 0.0.0.0:80")

    while True:
        try:
            cs, addr = s.accept()
            #print("New connection from", addr)

            request = cs.recv(1024)
            if not request:
                cs.close()
                continue

            try:
                data = ujson.loads(request)
                x = data.get("x")
                y = data.get("y")
                
                oled.fill(0)
                oled.text(f"X:{x}", 0, 0)
                oled.text(f"Y:{y}", 0, 10)
                oled.show()
                
                reset()
                if y == 0:
                    if (x == 0):
                        pwm_left.duty_u16(0)
                        pwm_right.duty_u16(0)
                    elif (x > 0):
                        pwm_left.duty_u16(engine(x))
                        pwm_right.duty_u16(engine(x))
                    else:
                        back()
                        pwm_left.duty_u16(engine(abs(x)))
                        pwm_right.duty_u16(engine(abs(x)))
                else:
                    if y > 0:
                        turn_left(y)
                    else:
                        turn_right(abs(y))

                response = ujson.dumps({"status": "ok", "x": x, "y": y})
                cs.send(response.encode())
            except Exception as e:
                print("JSON parse error:", e)
                cs.send(ujson.dumps({"status": "error", "msg": str(e)}).encode())

            cs.close()
        except Exception as e:
            print("Connection error:", e)
            sleep(1)