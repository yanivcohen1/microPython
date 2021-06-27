from machine import Pin
from time import sleep

led = Pin(1, Pin.OUT) # 2(simulation only for repl), Pin.OUT, Pin.PULL_UP
btn = Pin(0, Pin.IN) # # 0, Pin.IN, Pin.PULL_UP
led.on() # led is off -> on is off and off is on
# led.value()

def blink_fun(pin):
    if btn()==1: # btn not press -> on is off and off is on
        led.on()
        # led.value(0)
    else:
        led.off()
        # led.value(1)

btn.irq(blink_fun)
