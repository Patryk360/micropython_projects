from machine import Pin, Timer

class TurnSignals:
    def __init__(self, pin_left, pin_right, timer_num=1):
        self.led_l = Pin(pin_left, Pin.OUT)
        self.led_r = Pin(pin_right, Pin.OUT)
        
        self.led_l.off()
        self.led_r.off()
        
        self.blinking_left = False
        self.blinking_right = False
        
        self.timer = Timer(timer_num)
        self.is_running = False

    def _blink_callback(self, timer):
        if self.blinking_left:
            self.led_l.value(not self.led_l.value())
        else:
            self.led_l.off()

        if self.blinking_right:
            self.led_r.value(not self.led_r.value())
        else:
            self.led_r.off()

    def set_left(self, state: bool):
        self.blinking_left = state
        self._manage_timer()

    def set_right(self, state: bool):
        self.blinking_right = state
        self._manage_timer()

    def _manage_timer(self):
        if self.blinking_left or self.blinking_right:
            if not self.is_running:
                self.timer.init(period=500, mode=Timer.PERIODIC, callback=self._blink_callback)
                self.is_running = True
        else:
            if self.is_running:
                self.timer.deinit()
                self.is_running = False
                self.led_l.off()
                self.led_r.off()