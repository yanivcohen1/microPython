import user_lib.settings as settings
emulated = settings.isEmulated()
if emulated:
    from machine2 import Pin
else:
    from machine import Pin

import time

led = Pin(5, Pin.OUT)
while True:
    led.on()
    time.sleep(1)
    print("status:", led.value())
    led.off()
    time.sleep(1)
    print("status:", led.value())