import sys
sys.path.append("/libs")

from machine import Pin, SoftSPI, SoftI2C
from time import sleep_ms
from mfrc522 import MFRC522
from ssd1306 import SSD1306_I2C

cs = Pin(1, Pin.OUT)
cs.value(1)

sck = Pin(8, Pin.OUT)
mosi = Pin(10, Pin.OUT)
miso = Pin(9, Pin.OUT)
spi = SoftSPI(sck=sck, mosi=mosi, miso=miso)
sda = Pin(6, Pin.OUT)

rdr = MFRC522(spi, sda)
button = Pin(0, Pin.IN, Pin.PULL_UP)

password = "Patryk#1"
block = 8
padded = password + " " * (16 - len(password))
data = bytearray(padded.encode())

i2c = SoftI2C(scl=Pin(9), sda=Pin(8))
oled_width = 128
oled_height = 64
oled = SSD1306_I2C(oled_width, oled_height, i2c)

print("Trzymaj przycisk, aby ZAPISAĆ hasło.")

while True:
    stat, _ = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        stat, raw_uid = rdr.anticoll()
        if stat == rdr.OK:
            if rdr.select_tag(raw_uid) == rdr.OK:
                key = [0xFF] * 6
                if rdr.auth(rdr.AUTHENT1A, block, key, raw_uid) == rdr.OK:

                    if button.value() == 0:
                        rdr.write(block, data)
                        print("Zapisano hasło:", password)
                        
                        oled.fill(0)
                        oled.text("S: "+str(password), 0, 0)
                        oled.show()
                    else:
                        raw_data = rdr.read(block)
                        read_password = bytes(raw_data).decode().strip()
                        print("Odczytane hasło:", read_password)
                        
                        oled.fill(0)
                        oled.text("R: "+str(read_password), 0, 0)
                        oled.show()

                    rdr.stop_crypto1()
                else:
                    print("Błąd uwierzytelniania!")
            else:
                print("Nie udało się wybrać tagu.")

    sleep_ms(100)
