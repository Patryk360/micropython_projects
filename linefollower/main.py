import sys
sys.path.append("/libs")
sys.path.append("/mode")
import _thread

import auto
import manual

_thread.start_new_thread(auto.start, ())
_thread.start_new_thread(manual.start, ())