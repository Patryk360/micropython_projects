from libs.core import ULoRa
from machine import SPI, Pin, I2C
from libs.ssd1306 import SSD1306_I2C

spi = SPI(0, baudrate=5000000, polarity=0, phase=0, sck=Pin(18), mosi=Pin(19), miso=Pin(16))

i2c = I2C(0, scl=Pin(1), sda=Pin(0))
oled = SSD1306_I2C(128, 64, i2c)

pins = {
    "ss": 17,
    "reset": 27,
    "dio0": 28,
}

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

oled.fill(0)
oled.text(f"OK", 0, 0)
oled.show()

v = 0

while True:
    msg = lora.listen(timeout=5000)
    if msg:
        v +=1
        print("Odebrano:", msg.decode())
        oled.fill(0)
        oled.text(f"OK {v} {msg.decode()}", 0, 0)
        oled.show()