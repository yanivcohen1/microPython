from machine import Pin
# from esp import flash_size
# import re
# import micropython, gc
import uos

fs_stat = uos.statvfs('/')
fs_size = fs_stat[0] * fs_stat[2]

if fs_size == 2097152:
    # esp32 without spram - relay test
    relay = Pin(13, Pin.OUT, value=1)
    import user_lib.alive_btn_test
elif fs_size == 2072576:
    # esp32 with spram - led will power off on reset
    led = Pin(0, Pin.OUT, Pin.PULL_UP)
import ws