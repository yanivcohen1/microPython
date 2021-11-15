
simulation = False
try:
    from time import sleep
    import network
    from user_lib.encryption import decrypt
except:
    simulation = True

def wifi_connect():
    if not simulation:
        sta_if = network.WLAN(network.STA_IF)
        while not sta_if.isconnected():
            print('connecting to network...')
            try:
                sta_if.active(True)
                sta_if.connect("HOTBOX-89BA-yaniv", decrypt(b'C\xfcC\xe10>\xf8\xc4i\x88Da?\xd4\x82\x86'))
            except:
                sleep(10)
            # while not sta_if.isconnected():
                # pass
        print('network config:', sta_if.ifconfig())

# wifi_connect()
