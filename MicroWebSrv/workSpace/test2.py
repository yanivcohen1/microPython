from machine import Pin, ADC
import time

sliderPot = ADC(Pin(34))
sliderPot.atten(ADC.ATTN_11DB) # Full range: 3.3v

led = Pin(2, Pin.OUT) # pin 2(scool) insted of 5(yair)
while True:
    led.on()
    time.sleep(0.5)
    print("status:", led.value())
    led.off()
    time.sleep(0.5)
    print("status:", led.value())
    
    print("slider:", int(sliderPot.read() * 100 / 4095))