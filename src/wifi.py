name = "rssi"

from subprocess import Popen, PIPE # Used to run native OS commads in python wrapped subproccess
import numpy # Used for matrix operations in localization algorithm
from sys import version_info # Used to check the Python-interpreter version at runtime

# RSSI_Scan
    # Use:
        # from rssi import RSSI_Scan
        # rssi_scan_instance = RSSI_Scan('network_interface_name) 
    # -------------------------------------------------------
    # Description:
        # Allows a user to query all available accesspoints available.
        # User has the option of define a specific set of access 
        # points to query.
    # -------------------------------------------------------
    # Input: interface name
        # [ie. network interface names: wlp1s0m, docker0, wlan0] 
class RSSI_Scan(object):
    # Allows us to declare a network interface externally.
    def __init__(self, interface):
        self.interface = interface

    # getRawNetworkScan
        # Description:
            # Runs the Ubuntu command 'iwlist' to scan for available networks.
            # Returns the raw console window output (unparsed).
        # ----------------------------------------------------------------
        # Input: (optional) 
            #   sudo: bool; defaults to false. False will not refresh the 
            #         network interface upon query. Sudo=true will require 
            #         the user will need to enter a sudo password at runtime.
        # ----------------------------------------------------------------
        # Returns: Raw terminal output
            # {
            #     'output':'''wlp1s0    Scan completed :
            #   Cell 01 - Address: A0:3D:6F:26:77:8E
            #             Channel:144
            #             Frequency:5.72 GHz
            #             Quality=43/70  Signal level=-67 dBm  
            #             Encryption key:on
            #             ESSID:"ucrwpa"
            #             Bit Rates:24 Mb/s; 36 Mb/s; 48 Mb/s; 54 Mb/s
            #             Mode:Master
            #   Cell 02 - Address: A0:3D:6F:26:77:82
            #             Channel:1
            #             Frequency:2.412 GHz (Channel 1)
            #             Quality=43/70  Signal level=-67 dBm  
            #             Encryption key:on
            #             ESSID:"eduroam"
            #             Bit Rates:18 Mb/s; 24 Mb/s; 36 Mb/s; 48 Mb/s; 54 Mb/s
            #             Mode:Master''',
            #     'error':''
            # }
    def getRawNetworkScan(self, sudo=False):
        # Scan command 'iwlist interface scan' needs to be fed as an array.
        if sudo:
            scan_command = ['sudo','iwlist',self.interface,'scan']
        else:
            scan_command = ['iwlist',self.interface,'scan']
        # Open a subprocess running the scan command.
        scan_process = Popen(scan_command, stdout=PIPE, stderr=PIPE)
        # Returns the 'success' and 'error' output.
        (raw_output, raw_error) = scan_process.communicate() 
        # Block all execution, until the scanning completes.
        scan_process.wait()
        # Returns all output in a dictionary for easy retrieval.
        return {'output':raw_output,'error':raw_error}

    # getSSID
        # Description:
            # Parses the 'SSID' for a given cell.
        # -----------------------------------------------
        # Input: (Raw string)
            # 01 - Address: A0:3D:6F:26:77:8E
            # Channel:144
            # Frequency:5.72 GHz
            # Quality=43/70  Signal level=-67 dBm  
            # Encryption key:on
            # ESSID:"ucrwpa"
            # Bit Rates:24 Mb/s; 36 Mb/s; 48 Mb/s; 54 Mb/s
            # Mode:Master
        # -----------------------------------------------
        # Returns:
            # 'ucrwpa'
    @staticmethod
    def getSSID(raw_cell):
        ssid = raw_cell.split('ESSID:"')[1]
        ssid = ssid.split('"')[0]
        return ssid

    # getQuality
        # Description:
            # Parses 'Quality level' for a given cell.
        # -----------------------------------------------
        # Input: (Raw string)
            # 01 - Address: A0:3D:6F:26:77:8E
            # Channel:144
            # Frequency:5.72 GHz
            # Quality=43/70  Signal level=-67 dBm  
            # Encryption key:on
            # ESSID:"ucrwpa"
            # Bit Rates:24 Mb/s; 36 Mb/s; 48 Mb/s; 54 Mb/s
            # Mode:Master
        # -----------------------------------------------
        # Returns:
            # '43/70'
    @staticmethod
    def getFrequency(raw_cell):
        quality = raw_cell.split('Frequency:')[1]
        quality = quality.split(' ')[0]
        return float(quality)

    @staticmethod
    def getQuality(raw_cell):
        quality = raw_cell.split('Quality=')[1]
        quality = quality.split(' ')[0]
        return quality

    # getSignalLevel
        # Description:
            # Parses 'Signal level' for a given cell.
            # Measurement is in 'dBm'.
        # -----------------------------------------------
        # Input: (Raw string)
            # 01 - Address: A0:3D:6F:26:77:8E
            # Channel:144
            # Frequency:5.72 GHz
            # Quality=43/70  Signal level=-67 dBm  
            # Encryption key:on
            # ESSID:"ucrwpa"
            # Bit Rates:24 Mb/s; 36 Mb/s; 48 Mb/s; 54 Mb/s
            # Mode:Master
        # -----------------------------------------------
        # Returns: (string)
            # '-67'    
    @staticmethod
    def getSignalLevel(raw_cell):
        signal = raw_cell.split('Signal level=')[1]
        signal = int(signal.split(' ')[0])
        return signal

    # getMacAddress
        # Description:
            # Method returns the MAC address of the AP
        # -----------------------------------------------
        #   Input: (Raw string)
            # 01 - Address: A0:3D:6F:26:77:8E
            # Channel:144
            # Frequency:5.72 GHz
            # Quality=43/70  Signal level=-67 dBm  
            # Encryption key:on
            # ESSID:"ucrwpa"
            # Bit Rates:24 Mb/s; 36 Mb/s; 48 Mb/s; 54 Mb/s
            # Mode:Master
        # -----------------------------------------------
        # Returns: (string)
            #   'A0:3D:6F:26:77:8E'
    @staticmethod
    def getMacAddress(raw_cell):
        mac = raw_cell.split('Address: ')[1]
        mac = mac.split(' ')[0]
        mac = mac.strip()
        return mac

    # parseCell
        # Description:
            # Takes a raw cell string and parses it into a dictionary.
        # -----------------------------------------------
        # Input: (Raw string)
            # '''01 - Address: A0:3D:6F:26:77:8E
            # Channel:144
            # Frequency:5.72 GHz
            # Quality=43/70  Signal level=-67 dBm  
            # Encryption key:on
            # ESSID:"ucrwpa"
            # Bit Rates:24 Mb/s; 36 Mb/s; 48 Mb/s; 54 Mb/s
            # Mode:Master'''
        # -----------------------------------------------
        # Returns:
            # {
            #     'ssid':'ucrwpa',
            #     'quality':'43/70',
            #     'signal':'-67'
            # }    
    def parseCell(self, raw_cell):
        cell = {
            'ssid': self.getSSID(raw_cell),
            'quality': self.getQuality(raw_cell),
            'signal': self.getSignalLevel(raw_cell),
            'mac': self.getMacAddress(raw_cell),
            'frequency': self.getFrequency(raw_cell)
        }
        return cell

    # formatCells
        # Description:
            # Every network listed is considered a 'cell.
            # This function parses each cell into a dictionary.
            # Returns list of dictionaries. Makes use of 'parseCell'.
            # If not networks were detected, returns False.
        # -----------------------------------------------
        # Input: (Raw terminal string)
            # '''01 - Address: A0:3D:6F:26:77:8E
            # Channel:144
            # Frequency:5.72 GHz
            # Quality=43/70  Signal level=-67 dBm  
            # Encryption key:on
            # ESSID:"ucrwpa"
            # Bit Rates:24 Mb/s; 36 Mb/s; 48 Mb/s; 54 Mb/s
            # Mode:Master
            # 02 - Address: A0:3D:6F:26:77:8E
            # Channel:144
            # Frequency:5.72 GHz
            # Quality=30/70  Signal level=-42 dBm  
            # Encryption key:on
            # ESSID:"dd-wrt"
            # Bit Rates:24 Mb/s; 36 Mb/s; 48 Mb/s; 54 Mb/s
            # Mode:Master'''
        # -----------------------------------------------
        # Returns: (Array of dictionaries)
            # [
            #     {
            #         'ssid':'ucrwpa',
            #         'quality':'43/70',
            #         'signal':'-67'
            #     },
            #     {
            #         'ssid':'dd-wrt',
            #         'quality':'30/70',
            #         'signal':'-42'
            #     }
            # ]    
    def formatCells(self, raw_cell_string):
        try:
            raw_cell_string = raw_cell_string.decode()
        except:
            print('Already in string.')
        
        raw_cells = raw_cell_string.split('Cell') # Divide raw string into raw cells.
        raw_cells.pop(0) # Remove unneccesary "Scan Completed" message.
        if(len(raw_cells) > 0): # Continue execution, if atleast one network is detected.
            # Iterate through raw cells for parsing.
            # Array will hold all parsed cells as dictionaries.
            formatted_cells = [self.parseCell(cell) for cell in raw_cells]
            # Return array of dictionaries, containing cells.
            return formatted_cells
        else:
            print("Networks not detected.")
            return False
        # TODO implement function in ndoe to process this boolean (False)

    # filterAccessPoints
        # Description:
            # If the 'networks' parameter is passed to the 'getAPinfo'
            # function, then this method will filter out all irrelevant 
            # access-points. Access points specified in 'networks' array 
            # will be returned (if available).
        # -----------------------------------------------
        # Input: (Parsed array of cell dictionaries)
            # all_access_points = 
            # [
            #     {
            #         'ssid':'ucrwpa',
            #         'quality':'43/70',
            #         'signal':'-67'
            #     },
            #     {
            #         'ssid':'dd-wrt',
            #         'quality':'30/70',
            #         'signal':'-42'
            #     },
            #     {
            #         'ssid':'linksys',
            #         'quality':'58/70',
            #         'signal':'-24'
            #     }
            # ] 
            # network_names = (array of network names)
            # ['ucrwpa','dd-wrt']
        # -----------------------------------------------
        # Returns: (Array of dictionaries)
            # [
            #     {
            #         'ssid':'ucrwpa',
            #         'quality':'43/70',
            #         'signal':'-67'
            #     },
            #     {
            #         'ssid':'dd-wrt',
            #         'quality':'30/70',
            #         'signal':'-42'
            #     }
            # ] 
    @staticmethod
    def filterAccessPoints(all_access_points, network_names):
        focus_points = [] # Array holding the access-points of concern.
        # Iterate throguh all access-points found.
        for point in all_access_points:
            # Check if current AP is in our desired list.
            if point['ssid'] in network_names:
                focus_points.append(point)
        return focus_points
        # TODO implement something incase our desired ones were not found
 
    # getAPinfo
        # Description:
            # Method returns all (or chosen) available access points (in range).
            # Takes 2 optional parameters: 
            #   'networks' (array): 
            #       Lists all ssid's of concern. Will return only the available access 
            #       points listed here. If not provided, will return ALL access-points in range.        
            #   'sudo' (bool): 
            #       Whether of not method should use sudo privileges. If user uses sudo
            #       privileges, the network manager will be refreshed and will return 
            #       a fresh list of access-points available. If sudo is not provided, 
            #       a cached list will be returned. Cached list gets updated periodically.
        # -----------------------------------------------
        # Input: (Parsed array of cell dictionaries)
            # networks = (array of network names)
            # ['ucrwpa','dd-wrt']
            # sudo = True || False
        # -----------------------------------------------
        # Returns: (Array of dictionaries)
            # [
            #     {
            #         'ssid':'ucrwpa',
            #         'quality':'43/70',
            #         'signal':'-67'
            #     },
            #     {
            #         'ssid':'dd-wrt',
            #         'quality':'30/70',
            #         'signal':'-42'
            #     }
            # ] 
    def getAPinfo(self, networks=False, sudo=False):
        # TODO implement error callback if error is raise in subprocess
        # Unparsed access-point listing. AccessPoints are strings.
        raw_scan_output = self.getRawNetworkScan(sudo)['output']
        
        # Parsed access-point listing. Access-points are dictionaries.
        all_access_points = self.formatCells(raw_scan_output)
        # Checks if access-points were found.
        if all_access_points:
            # Checks if specific networks were declared.
            if networks:
                # Return specific access-points found.
                return self.filterAccessPoints(all_access_points, networks)
            else:
                # Return ALL access-points found.
                return all_access_points
        else:
            # No access-points were found. 
            return False
