# run os list
# import os
# print("os List:")
# print (os.listdir())
import user_lib.settings as settings
from machine import RTC
rtc = RTC()
# import datetime

def test():
    # current_time = datetime.datetime.now()
    year, monte, day, houre1, houre, mimite, secend, n = rtc.datetime()
    if year == 2000:
        print("error connect to ntptime remote server")
    # add time up to log
    log = "Up time: " +  str(day) + '-' + str(monte) + ' ' + str(houre+3) \
    + ':' + str(mimite) + ':' + str(secend) # 2018-03-29 10:26:23
    print(log)
    print("read it: \n") 
    for line in settings.readLinesFromLogFile():
        print(line)
    settings.appendLineToLogFile(str(log))
    print("verify it: \n") 
    for line in settings.readLinesFromLogFile():
        print(line)

test()
# print(settings.readLinesFromLogFile())