import triad_openvr
import time
from datetime import datetime
from statistics import mean 
import sys
import socket


# Examines output log to calculate frequency between reads from device
# Writes frequencies to a second text file after calculating
def getTiming(fName, wName):
    f = open(fName, 'r+')
    w = open(wName, 'w+')
    time1 = 0.0
    time2 = 0.0
    with open(fName) as x:
        for line in x:
            read = f.readline().split(',')      # get whole line as array, splitting by comma
            if len(read) > 6:               # checks to see if array was parsed correctly and had all of its elements before looking for time value
                time2 = read[7]
                
                if (float(time1) == 0):   # checks whether there is an initial time1 value
                    time1 = float(read[7])          # assigns initial time value to replace 0
                    
                if float(time2) - float(time1) > 0:          # new time value found
                    # time_string = "Time1: " + str(time1) + "\nTime2: " + str(time2)      # record time1 and time2 values
                    # w.write(time_string)
                    period = float(time2) - float(time1)        # calculate time elapsed
                    per_format = f'{period:.5f}'
                    frequency = 1 / period                      # calculate frequency
                    freq_format = f'{frequency:.2f}'
                    # timing_string = "Period: " + per_format + " seconds\nFrequency: " + freq_format + " Hz\n\n"
                    timing_string = freq_format + "\n"
                    w.write(timing_string)
                    time1 = float(read[7])              # time2 becomes new time1 to compare next value against
        f.close()
        w.close()


# Method for checking against output of getTiming() to see average frequency for a given log
def freqStability(fName):
    read = []
    f = open(fName, 'r+')
    with open(fName) as x:
        for line in x:
            freq = float(f.readline().strip())
            read.append(freq)     
    print("Average Frequency: ", (mean(read)), " Hz")
    f.close()


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
f.write(txt)    # drop this outside of while. fill array with values within loop, write after
f.close()


# Analysis #
writeFile = timestr.rstrip(".txt") + "-TIME.txt"
getTiming(timestr, writeFile)
# print(writeFile)
# freqStability(writeFile)

# Can we access the IMU directly? Are we limited to the rate of the base station? Might be slower than IMU
# Eye tracking features -- eye fields? additional data? 