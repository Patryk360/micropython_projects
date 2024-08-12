import network
import usocket as socket
from time import time, sleep
import ujson
from motorControler import motorSpeed, motorLeft, motorRight, motorStop
from imuControler import temperature, gyro
from servoControler import setServoDegree, getServoDegree
from distanseControler import distanse

s = None

def connectToAP(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    start_time = time()
    timeout = 5
    
    wlan.connect(ssid, password)
    
    while not wlan.isconnected():
        if time() - start_time > timeout:
            print("err")
            return
        sleep(1)
    
    print("CONECTED!")

def connectToBoat(ip, port):
    global s
    addr = (ip, port)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(addr)
    
    message = "HI!"
    s.send(message.encode())
    print('Wysłano:', message)
    
    while True:
        dataRes = s.recv(1024)
        if not dataRes:
            break
        temp = temperature()
        gyroData = ujson.loads(gyro())
        servo = getServoDegree()
        dis = distanse()
    
        dataJSON = {
            "gyro": {
                "x": gyroData["x"],
                "y": gyroData["y"],
                "z": gyroData["z"]
            },
            "temperature": temp,
            "servo": servo,
            "distanse": dis
        }
    
        data = ujson.dumps(dataJSON)
        s.send(data.encode())
        print(dataRes.decode())
        
        d = ujson.loads(dataRes.decode())
        setServoDegree((d['joystick']['x'] / 100) * 180)
        motorSpeed(d['motor']['speed'])
        motorLeft()