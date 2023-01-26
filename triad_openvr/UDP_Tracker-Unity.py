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

# Test UDP Send
# Unity_Listen_Port = 5123
# tx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# test_msg = "test"
# tx_sock.sendto(test_msg.encode(), (UDP_IP, Unity_Listen_Port))

def listenUDP():
    rx_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', 5124)
    rx_sock.bind(server_address)
    # rx_sock.bind(('localhost', 5124))
    text = ""
    while True:
        data, addr = rx_sock.recvfrom(1024)    # receives data as byte
        decoded = data.decode("utf-8")  # decode to UTF-8 to use as string in program
        message = decoded.strip("\n")
        if message == "start":
            t = threading.Thread(target=getTrackerData, args=(text,))
            t.start()

        elif message == "stop":
            t.join()
            now = datetime.now()
            timestr = now.strftime("%Y_%m_%d-%H_%M_%S.txt")
            with open(timestr, "w") as f:
                f.write(text)
            f.close()
            break


def getTrackerData():
    interval = 1/250    # desired refresh rate -- highest stable freq. is 250 Hz (1/250)
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
        text += str(time.time()) # Add CPU timestamp
        text += "\n"
        print(text)
        execution_time = time.time()
        while(time.time()-execution_time < interval):   # do nothing for rest of interval time if code executes too fast
            pass



try:
    # start listening
    t = threading.Thread(target=listenUDP)
    t.start()

except KeyboardInterrupt:
    t.stop()