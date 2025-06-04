import network
import socket
import ujson
from time import sleep
import config

SERVER_IP = "192.168.4.1"
SERVER_PORT = 80

def connect_wifi(ssid, password):
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

def send_mode(mode):
    try:
        addr = socket.getaddrinfo(SERVER_IP, SERVER_PORT)[0][-1]
        s = socket.socket()
        s.connect(addr)
        data = ujson.dumps({"mode": mode})
        s.send(data.encode())

        response = s.recv(1024)
        print("Response from server:", response.decode())
        s.close()
    except Exception as e:
        print("Socket error:", e)

def main():
    if connect_wifi(config.ssid, config.password):
        send_mode(1)

main()