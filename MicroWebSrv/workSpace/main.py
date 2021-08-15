from machine import Pin
# from esp import flash_size
# import re
# import micropython, gc
import uos
import machine
import ubinascii

device_unique_id = ubinascii.hexlify(machine.unique_id()).decode('utf-8')

if device_unique_id == '2462abe768e4':
    # esp32 without spram - relay test
    relay = Pin(13, Pin.OUT, value=1)
    import user_lib.alive_btn_test
elif device_unique_id == '7c9ebd288188':
    # esp32 with spram - led will power off on reset
    led = Pin(0, Pin.OUT, Pin.PULL_UP)

import ws