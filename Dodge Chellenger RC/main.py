import sys
sys.path.append("/libs")
from machine import Pin, SPI, I2C, PWM
from nrf24l01 import NRF24L01
from bme280_float import BME280
from utime import sleep_ms, sleep
import struct

RX_POLL_DELAY = const(15)
RESPONDER_SEND_DELAY = const(10)

i2c = I2C(scl=Pin(22), sda=Pin(21))
bme280 = BME280(i2c=i2c)

pwm = PWM(Pin(32))
pwm.freq(50)

def set_angle(angle):
    min_ns = 600_000
    max_ns = 2400_000
    pulse = min_ns + (max_ns - min_ns) * angle / 180
    pwm.duty_ns(int(pulse))

def left(percent):
    percent = min(max(percent, 0), 100)
    angle = 90 - ((90 - 65) * percent / 100)
    set_angle(angle)

def right(percent):
    percent = min(max(percent, 0), 100)
    angle = 90 + ((110 - 90) * percent / 100)
    set_angle(angle)

speaker = PWM(Pin(25))

def beep(freq, duration):
    speaker.freq(freq)
    speaker.duty(20)
    sleep(duration)
    speaker.duty(0)

#beep(100, 0.5)

RPWM = Pin(27, Pin.OUT)
LPWM = Pin(13, Pin.OUT)

R_EN = PWM(Pin(26))
R_EN.freq(20000)
L_EN = PWM(Pin(12))
L_EN.freq(20000)

def engine(percent, pot):
    max_pwm = int(pot * 1023 / 100)

    percent = max(min(percent, 100), -100)

    if percent > 0:
        pwm_val = int(abs(percent) * max_pwm / 100)
        print(percent)
        print(pwm_val)
        RPWM.on()
        LPWM.off()
        R_EN.duty(pwm_val)
        L_EN.duty(pwm_val)
    else:
        pwm_val = int(abs(percent) * max_pwm / 100)
        print(percent)
        print(pwm_val)
        RPWM.off()
        LPWM.on()
        R_EN.duty(pwm_val)
        L_EN.duty(pwm_val)

def responder():
    pipes = (b"21378", b"21379")
    spi = SPI(1, sck=Pin(18), mosi=Pin(23), miso=Pin(19))
    csn = Pin(5, mode=Pin.OUT)
    ce = Pin(17, mode=Pin.OUT)
    
    nrf = NRF24L01(spi, csn, ce, payload_size=32)
    nrf.open_tx_pipe(pipes[1])
    nrf.open_rx_pipe(1, pipes[0])
    nrf.start_listening()

    print("NRF24L01 responder: czekam na dane")

    while True:
        if nrf.any():
            received = nrf.recv()
            try:
                x_left, y_left, x_right, y_right, pot, beep_sw = struct.unpack(">bbbbbb", received)
                print(f"📥 Odebrano: ", (x_left, y_left, x_right, y_right, pot, beep_sw))
                
                engine(y_left, pot)
                percent_x_right = max(min(x_right, 100), -100)
                if percent_x_right >= 0:
                    right(percent_x_right)
                else:
                    left(abs(percent_x_right))

                temp, pres, hum = bme280.read_compensated_data()
                pres = pres / 100

                print(f"📊 Sensor BME280: Temp={temp:.2f} °C, Ciśnienie={pres:.2f} hPa, Wilgotność={hum:.2f}%")

                packet = struct.pack(">ff", temp, pres)

                sleep_ms(RESPONDER_SEND_DELAY)
                nrf.stop_listening()
                nrf.send(packet)
                print("📤 Odesłano dane:", temp, pres)

            except Exception as e:
                print("❌ Błąd dekodowania lub wysyłania:", e)

            nrf.start_listening()

        sleep_ms(RX_POLL_DELAY)

responder()