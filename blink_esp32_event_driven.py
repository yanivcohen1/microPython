
from machine import Pin

from time import sleep

  

led = Pin(1, Pin.OUT)

btn = Pin(0, Pin.IN)

led.on() # led is off -> on is off and off is on

  

def blink_fun(pin):

    if btn()==1: # btn not press -> on is off and off is on

        led.on()

    else:

        led.off()

    

btn.irq(blink_fun)
