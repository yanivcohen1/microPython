from machine import Pin, Timer
import time;

led = Pin(25, Pin.OUT)
tim = Timer()
def tick(timer):
    global led
    led.toggle()
    localtime = time.localtime(time.time())
    print ("Local current time :", localtime)

tim.init(freq=2.5, mode=Timer.PERIODIC, callback=tick)