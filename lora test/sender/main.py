from libs.core import ULoRa
from machine import SPI, Pin
from time import sleep

spi = SPI(1, baudrate=5000000, polarity=0, phase=0, sck=Pin(25), mosi=Pin(27), miso=Pin(26))
pins = {"ss": 14, "reset": 2, "dio0": 4}

parameters = {
    "frequency": 433000000,
    "frequency_offset": 0,
    "tx_power_level": 14,
    "signal_bandwidth": 125e3,
    "spreading_factor": 9,
    "coding_rate": 5,
    "preamble_length": 8,
    "implicitHeader": False,
    "sync_word": 0x2A,
    "enable_CRC": True,
    "invert_IQ": False,
}

lora = ULoRa(spi, pins, parameters)

v = 0

while True:
    v +=1
    print(f"TEST {v}")
    lora.println(f"TEST {v}")
    sleep(5)