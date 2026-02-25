from machine import Pin, Timer
import time

class SpeedSensor:
    def __init__(self, pin_num, diameter_m=0.06):
        self.pin = Pin(pin_num, Pin.IN, Pin.PULL_UP)
        self.circumference = diameter_m  # Masz już obwód w metrach
        self.v_kmh = 0.0
        self.last_time = time.ticks_ms()
        
        # Timer sprawdza co 500ms czy koło stoi
        self.timeout_timer = Timer(0)
        self.timeout_timer.init(period=500, mode=Timer.PERIODIC, callback=self._check_timeout)
        
        self.pin.irq(trigger=Pin.IRQ_FALLING, handler=self._pulse_callback)

    def _pulse_callback(self, pin):
        current_time = time.ticks_ms()
        delta_t = time.ticks_diff(current_time, self.last_time)
        
        if delta_t > 20: 
            self.v_kmh = (self.circumference / delta_t) * 3600
            self.last_time = current_time

    def _check_timeout(self, timer):
        if time.ticks_diff(time.ticks_ms(), self.last_time) > 2000:
            self.v_kmh = 0.0

    def get_speed(self):
        return self.v_kmh