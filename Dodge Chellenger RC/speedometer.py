import math
import time
from machine import Pin

class SpeedSensor:
    def __init__(self, pin_num, diameter_m=0.06):
        self.pin = Pin(pin_num, Pin.IN, Pin.PULL_UP)
        self.circumference = math.pi * diameter_m
        
        self.last_pulse_time = time.ticks_ms()
        self.delta_t = 0
        self.current_speed = 0.0
        
        self.pin.irq(trigger=Pin.IRQ_FALLING, handler=self._pulse_callback)

    def _pulse_callback(self, pin):
        now = time.ticks_ms()
        dt = time.ticks_diff(now, self.last_pulse_time)

        if dt > 15:
            self.delta_t = dt
            self.last_pulse_time = now

    def get_speed(self):
        if time.ticks_diff(time.ticks_ms(), self.last_pulse_time) > 2000:
            self.current_speed = 0.0
            self.delta_t = 0

        elif self.delta_t > 0:
            raw_speed = (self.circumference / self.delta_t) * 3600
            
            if self.current_speed == 0.0:
                self.current_speed = raw_speed
            else:
                self.current_speed = (self.current_speed * 0.7) + (raw_speed * 0.3)
                
        return self.current_speed