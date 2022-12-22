
def getTiming(fName):
    
    f = open(fName, 'r+')
    w = open('timing_output.txt', 'w+')
    time1 = 0.0
    time2 = 0.0
    for line in f:

        read = f.readline().split(',')      # get whole line as array, splitting by comma
        if len(read) > 6:               # checks to see if array was parsed correctly and had all of its elements before looking for time value
            # print(read[7])
                        
            if float(time1) == 0:               # checks whether there is an initial time1 value
                time1 = float(read[7])          # assigns initial time value to replace 0
                time2 = float(read[7])

            time2 = float(read[7])
        

            if float(time2) == float(time1):
                continue
                # print("\nDUPLICATE FOUND\n")
          
            if float(time2) - float(time1) > 0:          # checks whether time has changed
                # print("\nTime1: ", time1, "\nTime2: ", time2)
                time_string = "Time1: " + str(time1) + "\nTime2: " + str(time2) + "\n"
                w.write(time_string)
                period = float(time2) - float(time1)
                per_format = f'{period:.5f}'
                frequency = 1 / period
                freq_format = f'{frequency:.2f}'
                # print("Period: ", per_format, " seconds")
                # print("Frequency: ", freq_format, " Hz")
                timing_string = "Period: " + per_format + " seconds\nFrequency: " + freq_format + " Hz\n\n"
                w.write(timing_string)
                time1 = time2


            

    f.close()
    w.close()


logfile = input("Log File: ")
getTiming(logfile)