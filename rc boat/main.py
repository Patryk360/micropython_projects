import sys
sys.path.append("/libs")
sys.path.append("/controlers")
from time import sleep
import ujson
from motorControler import motorSpeed, motorLeft, motorRight, motorStop
from imuControler import temperature, gyro
from servoControler import setServoDegree, getServoDegree
#from radioControler import startListening
#import radioControler

motorSpeed(180)
motorLeft()
sleep(2)
motorRight()
sleep(2)
motorStop()

#startListening()
setServoDegree(11)
sleep(1)
print(str(getServoDegree()))

while True:
    print(temperature())
    data = ujson.loads(gyro())
    x = data["x"]
    y = data["y"]
    z = data["z"]
    print(f"X: {x} Y: {y} Z: {z} ")
    sleep(1)