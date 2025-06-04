import network
import socket
import ujson
import config
from time import sleep

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
            print("New connection from", addr)

            request = cs.recv(1024)
            if not request:
                cs.close()
                continue

            try:
                data = ujson.loads(request)
                mode = data.get("mode")
                print("Received mode:", mode)
                config.mode = mode

                response = ujson.dumps({"status": "ok", "mode": mode})
                cs.send(response.encode())
            except Exception as e:
                print("JSON parse error:", e)
                cs.send(ujson.dumps({"status": "error", "msg": str(e)}).encode())

            cs.close()
        except Exception as e:
            print("Connection error:", e)
            sleep(1)