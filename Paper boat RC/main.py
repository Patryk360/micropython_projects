import sys
sys.path.append("/libs")
from machine import Pin, SPI, I2C, PWM
from nrf24l01 import NRF24L01
from utime import sleep_ms
import struct
from imu import MPU6050
from ssd1306 import SSD1306_I2C

i2c = I2C(scl=Pin(9), sda=Pin(8))

RX_POLL_DELAY = const(15)
RESPONDER_SEND_DELAY = const(20)

imu = MPU6050(i2c)
oled = SSD1306_I2C(128, 64, i2c)

R_EN = PWM(Pin(2))
R_EN.freq(20000)
RPWM = Pin(3, Pin.OUT)
L_EN = PWM(Pin(1))
L_EN.freq(20000)
LPWM = Pin(0, Pin.OUT)

def responder():
    pipes = (b"\xe1\xf0\xf0\xf0\xf0", b"\xd2\xf0\xf0\xf0\xf0")
    spi = SPI(1, sck=Pin(4), mosi=Pin(6), miso=Pin(5))
    csn = Pin(21, mode=Pin.OUT, value=1)
    ce = Pin(20, mode=Pin.OUT, value=0)
    
    nrf = NRF24L01(spi, csn, ce, payload_size=32)
    nrf.open_tx_pipe(pipes[1])
    nrf.open_rx_pipe(1, pipes[0])
    nrf.start_listening()

    print("NRF24L01 responder: czekam na dane")
    
    oled.fill(0)
    oled.text("OK", 0, 0)
    oled.show()

    servo = PWM(Pin(7), freq=50)

    def set_angle(angle):
        min_duty = 40
        max_duty = 115
        
        duty = int(min_duty + (max_duty - min_duty) * angle / 180)
        servo.duty(duty)

    def percent_angle(percent):
        if percent < -100:
            percent = -100
        elif percent > 100:
            percent = 100
        angle = int((percent + 100) * 180 / 200)
        return angle

    def engine(y_right, pot):
        max_pwm = int((pot / 100) * 65535)
        max_pwm = max(0, min(65535, max_pwm))
        
        if y_right < 0:
            speed = int(-y_right / 100 * max_pwm)
            RPWM.on()
            LPWM.off()
            R_EN.duty_u16(speed)
        elif y_right > 0:
            speed = int(y_right / 100 * max_pwm)
            RPWM.off()
            LPWM.on()
            R_EN.duty_u16(speed)
        else:
            RPWM.off()
            R_EN.duty_u16(0)
            LPWM.off()
            R_EN.duty_u16(0)

    while True:
        if nrf.any():
            received = nrf.recv()
            try:
                x_left, y_left, x_right, y_right, pot = struct.unpack(">bbbbb", received)
                print(f"Odebrano: ", (x_left, y_left, x_right, y_right, pot))

                temp = imu.temperature
                
                set_angle(percent_angle(x_right))
                
                engine(y_right, pot)

                print(f"Sensor MPU6050: Temp={temp:.2f} °C")

                packet = struct.pack(">f", temp)

                sleep_ms(RESPONDER_SEND_DELAY)
                nrf.stop_listening()
                nrf.send(packet)
                print("Odesłano dane:", temp)

            except Exception as e:
                print("Błąd dekodowania lub wysyłania:", e)

            nrf.start_listening()

        sleep_ms(RX_POLL_DELAY)

responder()