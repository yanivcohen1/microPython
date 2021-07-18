
import network
import encryption

sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect("HOTBOX-89BA-yaniv", encryption.dencrypt('0x30353238373238353434'))
        while not sta_if.isconnected():
            pass

print('network config:', sta_if.ifconfig())


