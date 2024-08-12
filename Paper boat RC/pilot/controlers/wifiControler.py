from machine import I2C, Pin
import network
import socket
import json
from machine_i2c_lcd import I2cLcd
from time import sleep
from joystickControler import joystick


i2c = I2C(1, sda=Pin(21), scl=Pin(22), freq=100000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

def createWiFiAP(ssid, password):
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(ssid=ssid, password=password, authmode=3, channel=11)
    
    while not ap.active():
        sleep(0.5)

    print('AP config:', ap.ifconfig())

def startServer():
    serverSocket = socket.socket()
    serverSocket.bind(('0.0.0.0', 3333))
    serverSocket.listen(5)
    print('Serwer uruchomiony na porcie 3333')
    lcd.putstr("Server is on!")
    
    while True:
        clientSocket, addr = serverSocket.accept()
        print('Client connected from', addr)
        lcd.clear()
        lcd.putstr("Connected!")
        while True:
            dataRes = clientSocket.recv(1024)
            if not dataRes:
                break
            clientSocket.send(joystick().encode())
            print(dataRes.decode())