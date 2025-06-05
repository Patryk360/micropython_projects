import sys
sys.path.append("/libs")
sys.path.append("/mode")
sys.path.append("/database")
from time import sleep
import config

import manual
import auto

from functions import *

if config.mode == 1:
    manual.start()
else:
    auto.start()

while True:
    sleep(1)