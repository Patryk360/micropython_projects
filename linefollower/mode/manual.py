import network
import socket
from time import sleep
import config

def start():
    print("MANUAL")

    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(ssid=config.ssid, password=config.password, authmode=3, channel=10)

    print("Access Point active!")
    print("IP:", ap.ifconfig()[0])

    addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]

    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    print("Server run on 0.0.0.0:80")

    while True:
        cl, addr = s.accept()
        print("New conn", addr)

        request = cl.recv(1024)
        print("Res:", request)

        cl.send("hi")
        cl.close()