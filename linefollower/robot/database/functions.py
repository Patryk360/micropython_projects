from machine import Pin, SoftI2C
from eeprom import EEPROM
import ujson

i2c = SoftI2C(scl=Pin(9), sda=Pin(8))

eeprom = EEPROM(i2c=i2c)

def write_json(addr, obj):
    json_str = ujson.dumps(obj)
    json_bytes = json_str.encode('utf-8')

    if addr + len(json_bytes) > 32768:
        raise ValueError("JSON too large for EEPROM at given address")

    eeprom.write(addr, json_bytes)

def read_json(addr, max_len=256):
    raw_bytes = eeprom.read(addr, max_len)

    trimmed = raw_bytes.rstrip(b'\xFF')

    try:
        json_str = trimmed.decode('utf-8')
        return ujson.loads(json_str)
    except Exception as e:
        print("JSON decode error:", e)
        return None