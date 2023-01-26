import triad_openvr
import time
from datetime import datetime
from statistics import mean 
import sys
import struct
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('10.0.1.48', 8051)

v = triad_openvr.triad_openvr()
# v.print_discovered_objects()

if len(sys.argv) == 1:                                   # Default interval value -- sys.argv will always have a length of 1 by default. sys.argv contains the name of the file being run
    interval = 1/250
    # print("\nDefault Interval: ", str(interval))
elif len(sys.argv) == 2:                                 # Option to add time interval as argument when calling program via terminal
    interval = 1/float(sys.argv[1])
    # print("\nInterval Set To: ", str(sys.argv[1]))
else:
    # print("\nInvalid number of arguments")
    interval = False

# print("\n\n",v.devices,"\n\n")

# v.devices contents:
# {'hmd_1': <triad_openvr.vr_tracked_device object at 0x00000290BA5CD240>,                          VARJO
# 'tracker_1': <triad_openvr.vr_tracked_device object at 0x00000290BA5CD208>,                       VIVE TRACKER
# 'tracking_reference_1': <triad_openvr.vr_tracking_reference object at 0x00000290BA6D89E8>,        BASE STATION 1
# 'tracking_reference_2': <triad_openvr.vr_tracking_reference object at 0x00000290BA6D8A20>,        BASE STATION 2
# 'controller_1': <triad_openvr.vr_tracked_device object at 0x00000290BA6D8B38>}

# print("\n\n",v.devices["tracker_1"].get_pose_euler(), "\n\n")
# print("\n\n",v.devices["hmd_1"].get_pose_quaternion(), "\n\n")

now = datetime.now()
timestr = now.strftime("%Y_%m_%d-%H_%M_%S.txt")
# print("LOG:  ", timestr)
f = open(timestr, "w")

max = 60                    # duration of tracking
txt = ""
begin = time.time()         # time = 0
while(time.time()-begin < max): # while for program time limit
    # while(time.time()-start < interval):
        ### TRACKER SAMPLING ###
        # for each in v.devices["tracker_1"].get_pose_quaternion():
        #     txt += "%.4f" % each
        #     txt += ","
    for each in v.devices["hmd_1"].get_pose_quaternion():       # get tracker data
        sent = sock.sendto(struct.pack('d'*len(each), *each), server_address)
        txt += "%.4f" % each
        txt += ","
    #########################
    # End of tracker data -- append timestamp and add new line for next sample
    txt += str(time.time())
    txt += "\n"

    start = time.time()
    while(time.time()-start < interval):
        pass


f.write("Interval: " + str(interval) + "\nRun Time: " + str(max) + "\n")
f.write(txt)
f.close()