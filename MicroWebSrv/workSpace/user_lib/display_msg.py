import user_lib.sh1106 as ssd1306
from machine import Pin, I2C

# ESP32 Pin assignment 
# i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
i2c = I2C(scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SH1106_I2C(oled_width, oled_height, i2c) # SSD1306_I2C

def display(msg):
    oled.fill(0)
    oled.text(msg, 0, 0) # 16 lines
    oled.show()

# how to use it
# from user_lib.servo import tester
# from user_lib.display_msg import display
# tester(display)