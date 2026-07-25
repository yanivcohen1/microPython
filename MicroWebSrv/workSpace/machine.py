# C:\Users\yaniv\AppData\Local\Programs\Thonny\Lib\site-packages\thonny\plugins\micropython\api_stubs
import user_lib.settings as settings
emulated = settings.isEmulated()
if emulated:
    from machine_emulater import Pin, ADC, I2C, ssd1306, Timer, WDT, PWM, Signal, RTC
else:
    from machine_simulater import Pin, ADC, SoftI2C, I2C, ssd1306, Timer, WDT, PWM, Signal, RTC