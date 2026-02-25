import sys
sys.path.append("/libs")
from machine import Pin, SPI, I2C, ADC
from nrf24l01 import NRF24L01
from ssd1306 import SSD1306_I2C
from ADS1115 import *
from time import sleep, ticks_ms, ticks_diff
import struct

i2c = I2C(scl=Pin(9), sda=Pin(8))
adc = ADS1115(i2c=i2c)
adc.setVoltageRange_mV(ADS1115_RANGE_4096)
oled = SSD1306_I2C(128, 64, i2c)

pot_raw = ADC(Pin(0))

beep_sw = Pin(2, Pin.IN, Pin.PULL_UP)

def read(channel):
    adc.setCompareChannels(channel)
    adc.startSingleMeasurement()
    while adc.isBusy():
        pass
    res = adc.getRawResult()
    return res

def percent(raw, center_value=12960, min_value=0, max_value=26060, deadzone=5):
    if raw == center_value:
        return 0
    elif raw > center_value:
        val = round(((raw - center_value) / (max_value - center_value)) * 100)
    else:
        val = -round(((center_value - raw) / (center_value - min_value)) * 100)
        
    if -deadzone < val < deadzone:
        return 0
    return val

pipes = (b"21378", b"21379")

def oled_clear_and_text(lines):
    oled.fill(0)
    for i, line in enumerate(lines):
        oled.text(str(line), 0, i * 10)
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
        x_left = percent(read(ADS1115_COMP_0_GND))
        y_left = percent(read(ADS1115_COMP_1_GND))
        x_right = percent(read(ADS1115_COMP_2_GND))
        y_right = percent(read(ADS1115_COMP_3_GND))
        pot_percent = round((pot_raw.read_u16() / 65535) * 100)
        pot = round(pot_percent / 10) * 10

        packet = struct.pack(">bbbbbb", x_left, y_left, x_right, y_right, pot, beep_sw.value())

        nrf.stop_listening()
        try:
            print("→ Wysyłam dane:", (x_left, y_left, x_right, y_right, pot, beep_sw.value()))
            #oled_clear_and_text(["Wysylam dane", x_left, y_left, x_right, y_right, pot, beep_sw.value()])
            nrf.send(packet)
        except OSError as e:
            print("❌ Błąd wysyłania:", e)
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
                temp, pres, speed = struct.unpack(">fff", response)
                print("✅ Otrzymano dane:", (temp, pres, speed))
                oled_clear_and_text([f"T: {temp:.2f} C", f"P: {pres:.2f} hPa", f"S: {speed:.2f} km/h", f"Pot: {pot}"])
            except Exception as e:
                print("⚠️ Błąd dekodowania:", e)
                oled_clear_and_text(["Blad dekodowania"])

        sleep(0.05)