from time import sleep
from machine import RTC
import user_lib.settings as settings
from _thread import allocate_lock, start_new_thread

simulation = False
try:
	import ntptime
except:
	simulation = True
# update clock from internet
# synchronize with ntp
# need to be connected to wifi
def cb_updateClock(reset):
    global simulation
    log = None
    rtc = RTC()
    if not simulation:
        connect = False
        while not connect:
            try:
                ntptime.settime() # set the rtc datetime from the remote server	
                year, monte, day, houre1, houre, mimite, secend, n = rtc.datetime()
                if year == 2000:
                    print("error connect to ntptime remote server")
                # add time up to log
                log = reset + "time Up : " +  str(day) + '-' + str(monte) + ' ' + str(houre+3) \
                + ':' + str(mimite) + ':' + str(secend) # 2018-03-29 10:26:23
                connect =True
            except:
                print("update clock wait for the internet")
                sleep(10)
    else:
        log = rtc.datetime()
    print(log)
    settings.appendLineToLogFile(log)

def updateClock(reset = ""):
    start_new_thread(cb_updateClock, (reset,))