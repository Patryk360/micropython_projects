from machine import Pin, Timer, PWM

class Horn:
    def __init__(self, pin_num, timer_num=2):
        self.speaker = PWM(Pin(pin_num))
        self.speaker.duty(0)
        
        self.timer = Timer(timer_num)
        self.is_beeping = False

    def _stop_callback(self, timer):
        self.speaker.duty(0)
        self.is_beeping = False

    def beep(self, freq=600, duration_ms=500):
        if not self.is_beeping:
            self.speaker.freq(freq)
            self.speaker.duty(20)
            self.is_beeping = True
            
            self.timer.init(period=duration_ms, mode=Timer.ONE_SHOT, callback=self._stop_callback)

    def stop(self):
        self.timer.deinit()
        self.speaker.duty(0)
        self.is_beeping = False