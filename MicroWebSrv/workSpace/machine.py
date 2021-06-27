# C:\Users\yaniv\AppData\Local\Programs\Thonny\Lib\site-packages\thonny\plugins\micropython\api_stubs
import random
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