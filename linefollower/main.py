import sys
sys.path.append("/libs")
sys.path.append("/mode")
import _thread
from time import sleep
import config

import auto
import manual

_thread.start_new_thread(auto.start, ())
_thread.start_new_thread(manual.start, ())

while True:
    print(config.mode)
    sleep(2)