from machine import Pin, ADC, Signal
from time import sleep

# ESP32 witout spram
btn = Pin(0, Pin.IN)
def blink_fun(pin):
    led.on() if btn() else led.off() 

btn.irq(blink_fun)
led = Signal(Pin(27, Pin.OUT, value=1), invert=False)
