import sys
sys.path.append("/libs")
sys.path.append("/controlers")
from wifiControler import connectToAP, connectToBoat

connectToAP("PILOT_RC", "T7es7yeumU[WQFv#tWub")
connectToBoat("192.168.4.1", 3333)