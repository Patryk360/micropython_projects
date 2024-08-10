import sys
sys.path.append("/libs")
sys.path.append("/controlers")
from wifiControler import createWiFiAP, startServer

createWiFiAP("PILOT_RC", "T7es7yeumU[WQFv#tWub")
startServer()