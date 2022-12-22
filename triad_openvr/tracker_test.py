import triad_openvr
import time
import sys

v = triad_openvr.triad_openvr()
v.print_discovered_objects()
print("\n")

f = open("output_tyler.txt", "w")


if len(sys.argv) == 1:                                   # Default interval value -- sys.argv will always have a length of 1 by default. sys.argv contains the name of the file being run
    interval = 1/250                                     # .004 seconds --> 4ms
    # try 1/200 for 200Hz / 5ms ?
    print("Default Interval: ", str(interval))
elif len(sys.argv) == 2:                                 # Option to add time interval as argument when calling program via terminal
    interval = 1/float(sys.argv[1])
    print("Interval Set To: ", str(sys.argv[1]))
else:
    print("Invalid number of arguments")
    interval = False
    
if interval:                    # program begins once interval is established
    begin = time.time()         # time = 0
    max = 60                    # duration of tracking
    while(time.time()-begin < max):
        start = time.time()
        txt = ""
        for each in v.devices["tracker_1"].get_pose_quaternions():
            txt += "%.4f" % each
            txt += ","
        txt += str(time.time())
        f.write(txt)
        print("\r" + txt, end="")
        #sleep_time = interval-(time.time()-start)
        #if sleep_time>0:
        #    time.sleep(sleep_time)


f.close()