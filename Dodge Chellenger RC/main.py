import sys
sys.path.append("/libs")
from machine import Pin, SPI, I2C, PWM
from nrf24l01 import NRF24L01
from bme280_float import BME280
from time import sleep_ms, sleep, ticks_ms, ticks_diff
import struct

from speedometer import SpeedSensor
from blinkers import TurnSignals
from horn import Horn

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

r_en = Pin(26, Pin.OUT)
l_en = Pin(12, Pin.OUT)
r_en.value(1)
l_en.value(1)

rpwm = PWM(Pin(27), freq=20000)
lpwm = PWM(Pin(13), freq=20000)

def engine(percent, pot_val):
    max_duty = int(pot_val * 65535 / 100)
    percent = max(min(percent, 100), -100)
    duty_val = int(abs(percent) * max_duty / 100)

    if percent > 0:
        lpwm.duty_u16(0)
        rpwm.duty_u16(duty_val)
    elif percent < 0:
        rpwm.duty_u16(0)
        lpwm.duty_u16(duty_val)
    else:
        rpwm.duty_u16(0)
        lpwm.duty_u16(0)

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
    
    speed_sensor = SpeedSensor(pin_num=32, diameter_m=0.06)
    signals = TurnSignals(pin_left=15, pin_right=2)
    car_horn = Horn(pin_num=4, timer_num=2)

    last_receive_time = ticks_ms()
    failsafe_active = False

    while True:
        current_speed = speed_sensor.get_speed()
        current_time = ticks_ms()

        if nrf.any():
            received = nrf.recv()
            try:
                x_left, y_left, x_right, y_right, pot, beep_sw = struct.unpack(">bbbbbb", received)
                
                last_receive_time = current_time
                if failsafe_active:
                    print("Połączenie przywrócone!")
                    failsafe_active = False
                
                engine(y_left, pot)
                
                percent_x_right = max(min(x_right, 100), -100)
                if percent_x_right >= 0:
                    right(percent_x_right)
                else:
                    left(abs(percent_x_right))

                temp, pres, hum = bme280.read_compensated_data()
                pres = pres / 100
                
                if x_right < -50:
                    signals.set_left(True)
                    signals.set_right(False)
                elif x_right > 50:
                    signals.set_left(False)
                    signals.set_right(True)
                else:
                    signals.set_left(False)
                    signals.set_right(False)
                
                if not beep_sw: 
                    car_horn.beep(freq=400, duration_ms=500)

                packet = struct.pack(">fff", temp, pres, current_speed)
                sleep_ms(RESPONDER_SEND_DELAY)
                nrf.stop_listening()
                nrf.send(packet)
                nrf.start_listening()

            except Exception as e:
                print("Błąd dekodowania lub wysyłania:", e)

        else:
            if ticks_diff(current_time, last_receive_time) > 500:
                if not failsafe_active:
                    print("Brak sygnału! Uruchamiam FAILSAFE (zatrzymuję silniki)")
                    failsafe_active = True
                    
                    engine(0, 0) 
                    right(0) 
                    
                    signals.set_left(False)
                    signals.set_right(False)

        sleep_ms(RX_POLL_DELAY)

if __name__ == "__main__":
    responder()