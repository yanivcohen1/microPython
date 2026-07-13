
simulation = False
import json
# import settings
try:
    import user_lib.settings as settings
    from time import sleep
    import network
    # from user_lib.encryption import decrypt
except:
    simulation = True
    from pathlib import Path

env_file = "env.json"
if simulation:
    script_dir = Path(__file__).parent.parent
    env_file = script_dir / "env.json"
json_data = settings.readFromFile(env_file) # {"wifi_name": "TP-Link_F34F_5G", "wifi_pass": "73769835"}
wifi_data = json.loads(json_data)
print("wifi_name:", wifi_data["wifi_name"])

def wifi_connect():
    if not simulation:
        sta_if = network.WLAN(network.STA_IF)
        while not sta_if.isconnected():
            print('connecting to network...')
            try:
                sta_if.active(True)
                sta_if.connect(wifi_data["wifi_name"], wifi_data["wifi_pass"])
            except:
                sleep(10)
            # while not sta_if.isconnected():
                # pass
        print('network config:', sta_if.ifconfig())

# wifi_connect()
