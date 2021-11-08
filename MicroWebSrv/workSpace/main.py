from machine import Pin
# from esp import flash_size
# import re
# import micropython, gc
import uos
import machine
import ubinascii
from time import sleep
from machine import Pin, ADC, SoftI2C, Timer, I2C, WDT, PWM, Signal
device_unique_id = ubinascii.hexlify(machine.unique_id()).decode('utf-8')

def resetWifiRelay():
    print("restart wifi")
    bazzer = None # Signal(Pin(27, Pin.OUT, value=0), invert=False) # 
    relay = None # Signal(Pin(13, Pin.OUT, value=1), invert=True) # 
    if device_unique_id == '2462abe768e4': # the esp32NoSpRam
        # esp32 without spram - buzzer test
        bazzer = Signal(Pin(27, Pin.OUT, value=0), invert=False)
        relay = Signal(Pin(13, Pin.OUT, value=1), invert=True)
        onbord_btn = Pin(0, Pin.IN)
        def blink_fun(pin):
            bazzer.off() if onbord_btn() else bazzer.on() # butten is inverted
        onbord_btn.irq(blink_fun)
        # reset wifi on-off relay
        relay.on()
        sleep(3)
        relay.off()

if device_unique_id == '2462abe768e4':
    # esp32 without spram - buzzer test
    resetWifiRelay()
    import ws
elif device_unique_id == '7c9ebd288188':
    # esp32 with spram - led will power off on reset
    led = Pin(0, Pin.OUT, Pin.PULL_UP)
    import ws