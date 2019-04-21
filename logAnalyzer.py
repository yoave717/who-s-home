import datetime
import json
import os
import multiprocessing as mp
from multiprocessing import Process
from SyslogServer import runLogServer
from SyslogServer import LOG_FILE
from pprint import pprint as pp
from datetime import datetime as dt
import nmap
NODE_LOCATION = {"Cinema_Room_Mesh_Node": "Basement", "Basement_Hallway_Mesh_Node": "Basement",
                 "Kitchen_Mesh_Node": "Ground Floor", "Parents_Room_Mesh_Node": "Ground Floor" }

LOCATION_NOT_HOME = "Away"
LOCATION = "location"
MAC = "macAddress"
TIME_STAMP = "timeStamp"
DEVICES = "devices"
DEVICE_CONNECTED_KEYWORD = " authenticated"
CLIENT_LIST_FILE_NAME = "SIGNIFICANT_CLIENT_LIST.json"

SIGNIFICANT_CLIENT_LIST = {}

SIGNIFICANT_CLIENT_STATUS_LIST = {}

LENGTH_FROM_MAC_ADDRESS_TO_END_OF_LINE = 27

MAC_ADDRESS_LENGTH = len("00:00:00:00:00:00")

HOSTS = "192.168.0.150-255"

with open(CLIENT_LIST_FILE_NAME) as json_file:  
    SIGNIFICANT_CLIENT_LIST = json.load(json_file)


def main():
    print('main')
    try:
        mp.set_start_method('spawn')
        createStatusList()
        server = Process(target=runLogServer)
        server.daemon = True
        server.start()
        with open(LOG_FILE) as f:
            while True:
                line = f.readline()
                analyze(line)
    except (IOError, SystemExit):
        server.terminate()
        server.close()
        raise
    except KeyboardInterrupt:
        print ("Crtl+C Pressed. Shutting down.")
        server.terminate()
        server.close()


def analyze(line):
    if line:
        print("line")
        if line.find(DEVICE_CONNECTED_KEYWORD) != -1:
            print("new device")
            #new device connected
            isSignificantDevice(line)


def getLocation(line):
    for nodeName, location in NODE_LOCATION.items():
        if line.find(nodeName) != -1:
            return location
    return LOCATION_NOT_HOME

#checks if connected device belongs to a significant client
#If it does, updates client status in significant clients status dict, and retuns True
#else returns false
def isSignificantDevice(line):
    macAddress = line[(len(line) - 1 - (LENGTH_FROM_MAC_ADDRESS_TO_END_OF_LINE + MAC_ADDRESS_LENGTH)): (len(line) - 1 - LENGTH_FROM_MAC_ADDRESS_TO_END_OF_LINE)]
    print (macAddress)
    for client in SIGNIFICANT_CLIENT_LIST:
        for device, macAdd in SIGNIFICANT_CLIENT_LIST[client].items():
            if macAdd == macAddress:
                #significant device connected
                d = SIGNIFICANT_CLIENT_STATUS_LIST[client][DEVICES][device]
                d[LOCATION] = getLocation(line)
                d[TIME_STAMP] = dt.now()
                if device == "Phone":
                    #assuming the client is carrying the phone at any given time
                    SIGNIFICANT_CLIENT_STATUS_LIST[client][LOCATION] = d[LOCATION]
                    SIGNIFICANT_CLIENT_STATUS_LIST[client][TIME_STAMP] = d[TIME_STAMP]
                refreshClientStatusList()



def getDeviceIPv4Address(macAddress):
    target_mac = macAddress

    nm = nmap.PortScanner()

    nm.scan(hosts=HOSTS, arguments='-sP', sudo=True)
    print("nmap finish")
    host_list = nm.all_hosts()
    for host in host_list:
        if  'mac' in nm[host]['addresses']:
            print(host+' : '+nm[host]['addresses']['mac'])
            if target_mac == nm[host]['addresses']['mac']:
                print('Target Found')



def refreshClientStatusList():
    for client in SIGNIFICANT_CLIENT_STATUS_LIST:
        if SIGNIFICANT_CLIENT_STATUS_LIST[client][LOCATION] != LOCATION_NOT_HOME:
            #client should be home -> checking
            if dt.now() - SIGNIFICANT_CLIENT_STATUS_LIST[client][TIME_STAMP] > datetime.timedelta(seconds=30):
                getDeviceIPv4Address(SIGNIFICANT_CLIENT_STATUS_LIST[client][DEVICES]["Phone"][MAC])


#intilizeing significant clients status list based on provided client list file
def createStatusList():
    for client in SIGNIFICANT_CLIENT_LIST:
        SIGNIFICANT_CLIENT_STATUS_LIST[client] = {LOCATION: LOCATION_NOT_HOME,
                                                    TIME_STAMP: dt.now(),
                                                    DEVICES: {}}
        for device, macAdd in SIGNIFICANT_CLIENT_LIST[client].items():
            if macAdd:
                d = {
                    LOCATION: LOCATION_NOT_HOME,
                    TIME_STAMP: dt.now(),
                    MAC: macAdd
                    }
                SIGNIFICANT_CLIENT_STATUS_LIST[client][DEVICES][device] = d





if __name__ == '__main__':
    os.remove(LOG_FILE)
    open(LOG_FILE, 'w')
    main()



