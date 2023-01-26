# Full Python implementation of receiving START/STOP commands from Unity via UDP to start and stop logging of tracker data at ~250Hz into separate log
import os
import signal
import socket
import sys
import time
import threading
from datetime import datetime

import triad_openvr

# v = triad_openvr.triad_openvr()
now = datetime.now()

UDP_IP = "127.0.0.1"
Unity_Listen_Port = 5123
Unity_Send_Port = 5124
BUFFER = 1024

tx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

rx_sock.bind((UDP_IP, Unity_Send_Port))

# test_msg = "test"
# tx_sock.sendto(test_msg.encode(), (UDP_IP, Unity_Listen_Port))

# data, addr = sock.recvfrom(1024)    # receives data as byte
# print("received message (byte): %s" % data)
# decoded = data.decode("utf-8")  # decode to UTF-8 to use as string in program
# message = decoded.strip("\n")
# print("received message (string): %s" % message)

def getTrackerData():
    interval = 1/250    # desired refresh rate -- highest stable freq. is 250 Hz (1/250)
    txt = ""
    start = time.time()
    while(time.time()-start < interval):
        ### UNCOMMENT FOR TRACKER SAMPLING ###
        # for each in v.devices["tracker_1"].get_pose_quaternion():
        #     txt += "%.4f" % each
        #     txt += ","
        ### UNCOMMENT FOR HEADSET SAMPLING ###
        # for each in v.devices["hmd_1"].get_pose_quaternion():       # get tracker data
        #     txt += "%.4f" % each
        #     txt += ","
        #########################
        txt += str(time.time()) # Add CPU timestamp
        txt += "\n"
        print(txt)
        execution_time = time.time()
        while(time.time()-execution_time < interval):   # do nothing for rest of interval time if code executes too fast
            pass

def checkMessage():
    data, addr = rx_sock.recvfrom(1024)    # receives data as byte
    decoded = data.decode("utf-8")  # decode to UTF-8 to use as string in program
    message = decoded.strip("\n") 
    return message


try:
    while(True):
        # constantly check for new packet    
        data, addr = rx_sock.recvfrom(1024)    # receives data as byte
        decoded = data.decode("utf-8")  # decode to UTF-8 to use as string in program
        message = decoded.strip("\n")

        if("start" == message):
            while(message != "stop"):
                getTrackerData()
            # check for stop signal
            data, addr = rx_sock.recvfrom(1024)
            decoded = data.decode("utf-8")
            message = decoded.strip("\n")

        if ("stop" == message):
            now = datetime.now()
            timestr = now.strftime("%Y_%m_%d-%H_%M_%S.txt")
            # print("LOG:  ", timestr)
            f = open(timestr, "w")  # opens file for writing this instance
            f.write(txt)
            f.close()
            txt = ""
            print("stopping...")


except KeyboardInterrupt:
    sys.exit(0)