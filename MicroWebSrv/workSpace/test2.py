import user_lib.settings as settings
emulated = settings.isEmulated()
if emulated:
    from machine2 import Pin, ADC
else:
    from machine import Pin, ADC

import time

sliderPot = ADC(Pin(34))
sliderPot.atten(ADC.ATTN_11DB) # Full range: 3.3v

led = Pin(5, Pin.OUT)
while True:
    led.on()
    time.sleep(1)
    print("status:", led.value())
    led.off()
    time.sleep(1)
    print("status:", led.value())
    
    print("slider:", int(sliderPot.read() * 100 / 4095))