from machine import Pin
from esp import flash_size

if flash_size() < 4200000:
    # esp32 without spram - relay test
    relay = Pin(13, Pin.OUT, value=1)
    import user_lib.alive_btn_test
else:
    # esp32 with spram - led will power off on reset
    led = Pin(0, Pin.OUT, Pin.PULL_UP)
import ws