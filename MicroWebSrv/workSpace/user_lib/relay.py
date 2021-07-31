from machine import Pin, ADC, Signal
from time import sleep

def test():
    # 5v relay on esp32 pin 13
    relay_pin = Pin(13, Pin.OUT)
    relay = Signal(relay_pin, invert=True)

    while True:
        relay.on()
        sleep(2)
        relay.off()
        sleep(2)

# test it
# test()