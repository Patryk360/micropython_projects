import sys
sys.path.append("/libs")
sys.path.append("/controlers")
from time import sleep
import ujson
from motorControler import motorSpeed, motorLeft, motorRight, motorStop
from imuControler import temperature, gyro
from servoControler import setServoDegree, getServoDegree
from wifiControler import connectToAP, connectToBoat, send

setServoDegree(15)
sleep(1)
setServoDegree(90)
sleep(1)
print(str(getServoDegree()))

connectToAP("PILOT_RC", "T7es7yeumU[WQFv#tWub")
connectToBoat("192.168.4.1", 3333)

motorSpeed(180)
motorLeft()
sleep(2)
motorRight()
sleep(2)
motorStop()

while True:
    temp = temperature()
    data = ujson.loads(gyro())
    x = data["x"]
    y = data["y"]
    z = data["z"]
    send(f"X: {x} Y: {y} Z: {z} Temp: {temp} ")
    sleep(5)