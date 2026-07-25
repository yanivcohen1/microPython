# C:\Users\yaniv\AppData\Local\Programs\Thonny\Lib\site-packages\thonny\plugins\micropython\api_stubs
import json
from pathlib import Path

env_file = "env.json"
script_dir = Path(__file__).parent
env_file = script_dir / "env.json"
with open(env_file, 'r') as f:
        json_data = f.read()
env_data = json.loads(json_data)
emulated = env_data["emulated"]
print("emulated:", emulated)

if emulated:
    from machine_emulater import Pin, ADC, I2C, ssd1306, Timer, WDT, PWM, Signal, RTC
else:
    from machine_simulater import Pin, ADC, SoftI2C, I2C, ssd1306, Timer, WDT, PWM, Signal, RTC