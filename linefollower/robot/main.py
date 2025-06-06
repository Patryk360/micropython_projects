import sys
sys.path.append("/libs")
sys.path.append("/mode")
sys.path.append("/database")
from time import sleep

from machine import Pin

import manual
import auto

from functions import *

button = Pin(10, Pin.IN, Pin.PULL_UP)

if button.value() == 0:
    manual.start()
else:
    auto.start()