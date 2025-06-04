import sys
sys.path.append("/libs")
sys.path.append("/mode")
sys.path.append("/database")
import _thread
from time import sleep
import config

import auto
import manual

from functions import *

data = {
    "test": 0,
    "mode": 0 
}

write_json(0, data)

sleep(1)
read_data = read_json(0)

print(read_data["test"])
print(read_data)

_thread.start_new_thread(auto.start, ())
_thread.start_new_thread(manual.start, ())

while True:
    sleep(1)