from src import wifi

interface = 'wlp58s0'
rssi_scanner = wifi.RSSI_Scan(interface)
wifi_scanned = rssi_scanner.getAPinfo()
for i, ws in enumerate(wifi_scanned):
    print('Wifi Counter: {}'.format(i+1))
    print(wifi_scanned[i])
