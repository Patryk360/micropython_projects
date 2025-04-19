import network
import socket
from time import sleep

def start():
    print("MANUAL")

    ssid = "LINEFOLLOWER"
    password = "linefollower#557"

    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(ssid=ssid, password=password, authmode=3, channel=11)

    while not ap.active():
        print("Starting...")
        sleep(1)

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