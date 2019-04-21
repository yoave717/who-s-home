import datetime
import json
from pprint import pprint as pp

NODE_LOCATION = {"Cinema_Room_Mesh_Node": "Basement", "Basement_Hallway_Mesh_Node": "Basement",
                 "Kitchen_Mesh_Node": "Ground Floor", "Parents_Room_Mesh_Node": "Ground Floor" }

LOCATION_NOT_HOME = "Away"

DEVICE_CONNECTED_KEYWORD = "authenticated"

CLIENT_LIST_FILE_NAME = "SIGNIFICANT_CLIENT_LIST.json"

SIGNIFICANT_CLIENT_LIST = {}

SIGNIFICANT_CLIENT_STATUS_LIST = {}

with open(CLIENT_LIST_FILE_NAME) as json_file:  
    SIGNIFICANT_CLIENT_LIST = json.load(json_file)

def main():
    try:
        createStatusList()
        pp(SIGNIFICANT_CLIENT_LIST)
        pp(SIGNIFICANT_CLIENT_STATUS_LIST)
        with open('syslog.log') as f:
            while True:
                line = f.readline()
                if line:
                    if line.find(DEVICE_CONNECTED_KEYWORD) != -1:
                        #new device connected
                        isSiginicantDevice(line)
                print (line)
    except (IOError, SystemExit):
        raise
    except KeyboardInterrupt:
        print ("Crtl+C Pressed. Shutting down.")


def createStatusList():
    for client in SIGNIFICANT_CLIENT_LIST:
        SIGNIFICANT_CLIENT_STATUS_LIST[client] = {"location": "", "timeStamp": 0, "devices": []}
        for device, macAdd in SIGNIFICANT_CLIENT_LIST[client].items():
            if macAdd:
                d = {"device": device, "location": "", "timeStamp": 0}
                SIGNIFICANT_CLIENT_STATUS_LIST[client]["devices"].append(d)



#checks if connected device belongs to a significant client
#If it does, updates client status in significant clients status dict, and retuns True
#else returns false
def isSiginicantDevice(line:str) -> bool:
    return

if __name__ == '__main__':
    main()



