from machine import Pin, I2C
from imu import MPU6050
i2c_mtu = I2C(0, sda=Pin(12), scl=Pin(13), freq=400000)
imu = MPU6050(i2c_mtu)
import ujson

def temperature():
    return str(round(imu.temperature,2))

def gyro():
    data = {
        "x": imu.gyro.x,
        "y": imu.gyro.y,
        "z": imu.gyro.z
    }
    return ujson.dumps(data)