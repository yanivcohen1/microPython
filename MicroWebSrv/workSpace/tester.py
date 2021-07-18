from machine import Pin, I2C
from user_lib import SSD1315_OLED_DISP

# using default address 0x3C
i2c = I2C(sda=Pin(21), scl=Pin(22))
display = SSD1315_OLED_DISP.SSD1306_I2C(128, 64, i2c)

# Print Hello World on the first line:
display.text('Hello, World!', 0, 0, 1)
display.show()