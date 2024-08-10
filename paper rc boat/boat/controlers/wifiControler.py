import network
import usocket as socket
from time import time, sleep

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
    
    #message = "Hello, Server!"
    #s.send(message.encode())
    #print('Wysłano:', message)
    
    #data = s.recv(1024)
    #print('Odebrano:', data.decode())

def send(msg):
    if s: s.send(msg)