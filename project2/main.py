from libs.core import ULoRa
from machine import SPI, Pin, I2C
from libs.ssd1306 import SSD1306_I2C

spi = SPI(1, baudrate=1000000, polarity=0, phase=0, sck=Pin(4), mosi=Pin(6), miso=Pin(5))

i2c = I2C(0, scl=Pin(9), sda=Pin(8))
oled = SSD1306_I2C(128, 64, i2c)

pins = {
    "ss": 3,
    "reset": 1,
    "dio0": 10,
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

lora.receive()

oled.fill(0)
oled.text(f"OK", 0, 0)
oled.show()

v = 0

def oled_print(oled, text, x=0, y=0, max_chars=16, line_height=8):
    lines = []
    while len(text) > max_chars:
        lines.append(text[:max_chars])
        text = text[max_chars:]
    lines.append(text)

    for i, line in enumerate(lines[:8]):
        oled.text(line, x, y + i * line_height)

while True:
    if lora.received_packet():
        msg = lora.read_payload()
        print("Odebrano:", msg.decode())
        v +=1
        text = f"{v} {msg.decode()}"
        oled.fill(0)
        oled_print(oled, text)
        oled.show()