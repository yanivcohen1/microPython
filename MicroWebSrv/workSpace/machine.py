# C:\Users\yaniv\AppData\Local\Programs\Thonny\Lib\site-packages\thonny\plugins\micropython\api_stubs
import random
import subprocess
from time import sleep
class Pin :
    IN=1
    OUT=2
    def __init__(self, pinNumber, pinDirection=1):
        def randoms(self):
            random.randint(0, 1)
        return None

    def on(self):
        return 0

    def off(self):
        return 1

    def irq(self, btn_change):
        return None

    def value(self):
        return random.randint(0, 1)

class ADC :
    ATTN_11DB=1
    def __init__(self, pinNumber):
        def randoms(self):
            random.randint(0, 1)
        return None

    def atten(self, atten):
        pass

    def read(self):
        return random.randint(0, 4095)

class SoftI2C:
    def __init__(self, scl=1, sda=2):
        return None

class ssd1306:
    def __init__(self):
        pass
    def SSD1306_I2C(self,a,b):
        return ssd1306()
    def SH1106_I2C(self,a,b):
        return ssd1306()
    def text(self,a,b,c):
        pass
    def show(self):
        pass
    def sleep(self,a):
        pass
    def fill(self,a):
        pass


def time_pulse_us(pin, level):
    return random.randint(1, int(100*2/0.034))

def sleep_us(num):
    sleep(num/1000000)
