
def getTiming(fName, wName):
    f = open(fName, 'r+')
    w = open(wName, 'w+')
    time1 = 0.0
    time2 = 0.0
    for line in f:
        read = f.readline().split(',')      # get whole line as array, splitting by comma
        if len(read) > 6:               # checks to see if array was parsed correctly and had all of its elements before looking for time value
            if float(time1) == 0:               # checks whether there is an initial time1 value
                time1 = float(read[7])          # assigns initial time value to replace 0
                time2 = float(read[7])

            time2 = float(read[7])
        
            if float(time2) == float(time1):    # skip duplicate time values
                continue
          
            if float(time2) - float(time1) > 0:          # new time value found
                time_string = "Time1: " + str(time1) + "\nTime2: " + str(time2) + "\n"      # record time1 and time2 values
                w.write(time_string)
                period = float(time2) - float(time1)        # calculate time elapsed
                per_format = f'{period:.5f}'
                frequency = 1 / period                      # calculate frequency
                freq_format = f'{frequency:.2f}'
                timing_string = "Period: " + per_format + " seconds\nFrequency: " + freq_format + " Hz\n\n"
                w.write(timing_string)
                time1 = time2               # time2 becomes new time1 to compare next value against
    f.close()
    w.close()


logfile = input("Log File: ")
writeFile = logfile.rstrip(".txt") + "-TIME.txt"
getTiming(logfile, writeFile)