import triad_openvr
import time
from datetime import datetime
import sys
# import socket

v = triad_openvr.triad_openvr()
v.print_discovered_objects()

if len(sys.argv) == 1:                                   # Default interval value -- sys.argv will always have a length of 1 by default. sys.argv contains the name of the file being run
    interval = 1/250                                     # .004 seconds --> 4ms
    # try 1/200 for 200Hz / 5ms ?
    print("\nDefault Interval: ", str(interval))
elif len(sys.argv) == 2:                                 # Option to add time interval as argument when calling program via terminal
    interval = 1/float(sys.argv[1])
    print("\nInterval Set To: ", str(sys.argv[1]))
else:
    print("\nInvalid number of arguments")
    interval = False

# print("\n\n",v.devices,"\n\n")

# v.devices contents:
# {'hmd_1': <triad_openvr.vr_tracked_device object at 0x00000290BA5CD240>,                          VARJO
# 'tracker_1': <triad_openvr.vr_tracked_device object at 0x00000290BA5CD208>,                       VIVE TRACKER
# 'tracking_reference_1': <triad_openvr.vr_tracking_reference object at 0x00000290BA6D89E8>,        BASE STATION 1
# 'tracking_reference_2': <triad_openvr.vr_tracking_reference object at 0x00000290BA6D8A20>,        BASE STATION 2
# 'controller_1': <triad_openvr.vr_tracked_device object at 0x00000290BA6D8B38>}

# print("\n\n",v.devices["tracker_1"].get_pose_euler(), "\n\n")
print("\n\n",v.devices["hmd_1"].get_pose_quaternion(), "\n\n")

now = datetime.now()
timestr = now.strftime("%Y_%m_%d-%H_%M_%S.txt")
print("LOG:  ", timestr)
f = open(timestr, "w")


if interval:                    # program begins once interval is established
    begin = time.time()         # time = 0
    max = 10                    # duration of tracking
    txt = ""
    while(time.time()-begin < max):
        start = time.time()
        
        # for each in v.devices["tracker_1"].get_pose_quaternion():
        #     txt += "%.4f" % each
        #     txt += ","
        for each in v.devices["hmd_1"].get_pose_quaternion():
            txt += "%.4f" % each
            txt += ","            
            
        txt += str(time.time())
        txt += "\n"

        # sleep_time = interval-(time.time()-start)
        # if sleep_time>0:
        #    time.sleep(sleep_time)
    f.write("Interval: " + str(interval) + "\nRun Time: " + str(max) + "\n")
    f.write(txt)    # drop this outside of while. fill array with values within loop, write after

f.close()


# Can we access the IMU directly? Are we limited to the rate of the base station? Might be slower than IMU
# Eye tracking features -- eye fields? additional data? 