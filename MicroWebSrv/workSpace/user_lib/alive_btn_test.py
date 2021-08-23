from machine import Pin, ADC, Signal
from time import sleep

# ESP32 witout spram 0=internal_btn, 1=internal_led
btn = Pin(0, Pin.IN)
def blink_fun(pin):
    led.off() if btn() else led.on() 

btn.irq(blink_fun)
led = Signal(Pin(27, Pin.OUT, value=0), invert=False) # relay 3 click tset
