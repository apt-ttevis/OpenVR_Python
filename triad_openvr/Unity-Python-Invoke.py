from datetime import datetime

now = datetime.now()
timestr = now.strftime("%Y_%m_%d-%H_%M_%S.txt")
# print("LOG:  ", timestr)
f = open(timestr, "w")

f.write("Hello World!")

f.close()

example = input("type something... is this working?")