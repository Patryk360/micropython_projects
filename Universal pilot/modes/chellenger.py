import sys
sys.path.append("/libs")
from machine import Pin, SPI, I2C
from nrf24l01 import NRF24L01
from ssd1306 import SSD1306_I2C
from time import sleep, ticks_ms, ticks_diff
import struct

i2c = I2C(scl=Pin(9), sda=Pin(8))
oled = SSD1306_I2C(128, 64, i2c)

pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")

def oled_clear_and_text(lines):
    oled.fill(0)
    for i, line in enumerate(lines):
        oled.text(line, 0, i * 10)
    oled.show()

def start():
    spi = SPI(1, sck=Pin(4), mosi=Pin(6), miso=Pin(5))
    csn = Pin(21, mode=Pin.OUT, value=1)
    ce = Pin(20, mode=Pin.OUT, value=0)

    nrf = NRF24L01(spi, csn, ce, payload_size=32)
    nrf.open_tx_pipe(pipes[0])
    nrf.open_rx_pipe(1, pipes[1])
    nrf.start_listening()

    print("NRF24L01 initiator: wysyłanie danych i oczekiwanie na odpowiedź")

    while True:
        temp = 24.7
        hum = 52.0

        packet = struct.pack(">ff", temp, hum)

        nrf.stop_listening()
        try:
            print("→ Wysyłam dane:", (temp, hum))
            oled_clear_and_text(["Wysylam dane", f"T: {temp:.2f} C", f"H: {hum:.2f} %"])
            nrf.send(packet)
        except OSError:
            print("❌ Błąd wysyłania")
            oled_clear_and_text(["Blad wysylania"])

        nrf.start_listening()

        start_time = ticks_ms()
        while not nrf.any():
            if ticks_diff(ticks_ms(), start_time) > 250:
                print("⏱️ Brak odpowiedzi")
                oled_clear_and_text(["Brak odpowiedzi"])
                break

        if nrf.any():
            try:
                response = nrf.recv()
                temp, pres = struct.unpack(">ff", response)
                print("✅ Otrzymano dane:", (temp, pres))
                oled_clear_and_text([f"T: {temp:.2f} C", f"P: {pres:.2f} hPa"])
            except Exception as e:
                print("⚠️ Błąd dekodowania:", e)
                oled_clear_and_text(["Blad dekodowania"])

        sleep(1)