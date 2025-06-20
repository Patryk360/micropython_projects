import sys
sys.path.append("/libs")
from machine import Pin, SoftSPI, SoftI2C
from nrf24l01 import *
from ssd1306 import SSD1306_I2C
from ADS1115 import *
import ujson
from time import sleep

spi = SoftSPI(sck=Pin(4), mosi=Pin(6), miso=Pin(5))
csn = Pin(21, Pin.OUT)
ce = Pin(20, Pin.OUT)

i2c = SoftI2C(scl=Pin(9), sda=Pin(8))
oled = SSD1306_I2C(128, 64, i2c)
adc = ADS1115(i2c=i2c)
adc.setVoltageRange_mV(ADS1115_RANGE_4096)

nrf = NRF24L01(spi, csn, ce, payload_size=32, channel=46)

def read(channel):
    adc.setCompareChannels(channel)
    adc.startSingleMeasurement()
    while adc.isBusy():
        pass
    res = adc.getRawResult()
    return res

def start():
    nrf.open_tx_pipe(b'\xe1\xf0\xf0\xf0\xf0')
    nrf.set_power_speed(POWER_0, SPEED_2M)
    nrf.stop_listening()
    oled.fill(0)
    oled.text("Nadajnik uruchomiony", 0, 0)
    oled.show()
    while True:
        data = {
            "t": read(ADS1115_COMP_0_GND),
            "s": 1,
        }

        try:
            json_bytes = ujson.dumps(data).encode("utf-8")
            if len(json_bytes) <= 32:
                nrf.send(json_bytes)
                print("Wysłano:", data)
                oled.fill(0)
                oled.text("Wyslano:", 0, 0)
                oled.text(str(read(ADS1115_COMP_0_GND)), 0, 10)
                oled.show()
            else:
                print("Dane za długie:", len(json_bytes), "bajtów")
        except Exception as e:
            print("Błąd kodowania JSON:", e)
        sleep(0.01)