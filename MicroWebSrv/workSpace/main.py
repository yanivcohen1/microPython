from machine import Pin
# led will power off on reset
led = Pin(0, Pin.OUT, Pin.PULL_UP)
# relay = Pin(13, Pin.OUT, value=1)
import ws