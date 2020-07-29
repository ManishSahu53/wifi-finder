import rssi
import numpy as np

interface = 'wlp1s0'
rssi_scanner = rssi.RSSI_Scan(interface)

# sudo argument automatixally gets set for 'false', if the 'true' is not set manually.
# python file will have to be run with sudo privileges.
ap_info = rssi_scanner.getAPinfo(sudo=True)

sx, sy = np.random.randint(0, 100, 1), np.random.randint(0, 100, 1)
print(ap_info)
