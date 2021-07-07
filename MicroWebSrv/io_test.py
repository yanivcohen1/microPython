import time
from machine import Pin

def io_flash(io):
    Pin(io,Pin.OUT,value=0)
    time.sleep_ms(200)
    Pin(io,Pin.OUT,value=1)

io_scl=[22,21]
io_tft=[12,14,18,19,23,27,33,32]
io_sd=[19,18,23,4]

Pin(5, Pin.OUT) #led on

while(1):
    # SCL port test.
    # p22.value(1)
    # time.sleep_ms(200)
    # p22.value(0)
    # time.sleep_ms(200)
    # p21.value(0)
    for i in io_scl:
        io_flash(i)
    # TFT port test
    for i in io_tft:
        io_flash(i)
    time.sleep_ms(1000)
    # Micro SD port test
    for i in io_sd:
        io_flash(i)