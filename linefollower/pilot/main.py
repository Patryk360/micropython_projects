import sys
sys.path.append("/libs")

import network
import socket
import ujson
from time import sleep
from machine import Pin, SoftI2C
import config
from ADS1115 import *
from ssd1306 import SSD1306_I2C

i2c = SoftI2C(scl=Pin(9), sda=Pin(8))
adc = ADS1115(i2c=i2c)
adc.setVoltageRange_mV(ADS1115_RANGE_4096)

i2c = SoftI2C(scl=Pin(9), sda=Pin(8))
oled = SSD1306_I2C(128, 64, i2c)

SERVER_IP = "192.168.4.1"
SERVER_PORT = 80
JOY_RANGE = 13200

def read(channel):
    adc.setCompareChannels(channel)
    adc.startSingleMeasurement()
    while adc.isBusy():
        pass
    res = adc.getRawResult()
    return res

def connect_wifi(ssid, password):
    try:
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        if not wlan.isconnected():
            print("Connecting to WiFi...")
            wlan.connect(ssid, password)
            for _ in range(20):
                if wlan.isconnected():
                    break
                sleep(0.5)
        if wlan.isconnected():
            print("Connected with IP:", wlan.ifconfig()[0])
            return True
        else:
            print("Failed to connect")
            return False
    except OSError as e:
            print(f"{e}")

def send_mode(x, y):
    try:
        addr = socket.getaddrinfo(SERVER_IP, SERVER_PORT)[0][-1]
        s = socket.socket()
        s.connect(addr)
        data = ujson.dumps({"x": x, "y": y})
        s.send(data.encode())

        response = s.recv(1024)
        print("Response from server:", response.decode())
        s.close()
    except Exception as e:
        print("Socket error:", e)

def scale_to_percent(value, center):
    delta = value - center
    percent = int((delta / JOY_RANGE) * 100)
    return max(min(percent, 100), -100) 

def main():
    centerX = read(ADS1115_COMP_0_GND)
    centerY = read(ADS1115_COMP_1_GND)
    if connect_wifi(config.ssid, config.password):
        while True:
            x = scale_to_percent(read(ADS1115_COMP_0_GND), centerX)
            y = scale_to_percent(read(ADS1115_COMP_1_GND), centerY)
            
            oled.fill(0)
            oled.text(f"X:{x}", 0, 0)
            oled.text(f"Y:{y}", 0, 10)
            oled.show()
            
            print(read(ADS1115_COMP_0_GND))
            print(x)
            print(y)
            send_mode(x, y)

main()