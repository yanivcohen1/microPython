# Write your code here :-)
from machine import Timer, Pin
from time import sleep_ms
import ubluetooth


class BLE:
    def __init__(self, name, rcv_trn_led):

        self.name = name
        self.ble = ubluetooth.BLE()
        self.ble.active(True)

        self.led = rcv_trn_led 
        self.timer1 = Timer(0)
        self.timer2 = Timer(1)

        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()

    def connected(self):

        self.timer1.deinit()
        self.timer2.deinit()

    def disconnected(self):

        self.timer1.init(
            period=1000, mode=Timer.PERIODIC, callback=lambda t: self.led(1)
        )
        sleep_ms(200)
        self.timer2.init(
            period=1000, mode=Timer.PERIODIC, callback=lambda t: self.led(0)
        )

    def ble_irq(self, event, data):

        if event == 1:
            """Central disconnected"""
            self.connected()
            self.led(1)

        elif event == 2:
            """Central disconnected"""
            self.advertiser()
            self.disconnected()

        elif event == 4:
            """New message received"""

            buffer = self.ble.gatts_read(self.rx)
            message = buffer.decode("UTF-8")[:-1]
            print(message)

            # no need print msg to REPL
            # if received == 'blue_led':
            #    blue_led.value(not blue_led.value())

    def register(self):

        # Nordic UART Service (NUS)
        NUS_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
        RX_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
        TX_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

        BLE_NUS = ubluetooth.UUID(NUS_UUID)
        BLE_RX = (ubluetooth.UUID(RX_UUID), ubluetooth.FLAG_WRITE)
        BLE_TX = (ubluetooth.UUID(TX_UUID), ubluetooth.FLAG_NOTIFY)

        BLE_UART = (
            BLE_NUS,
            (
                BLE_TX,
                BLE_RX,
            ),
        )
        SERVICES = (BLE_UART,)
        (
            (
                self.tx,
                self.rx,
            ),
        ) = self.ble.gatts_register_services(SERVICES)

    def send(self, data):
        self.ble.gatts_notify(0, self.tx, data + "\n")

    def advertiser(self):
        name = bytes(self.name, "UTF-8")
        self.ble.gap_advertise(
            100, bytearray("\x02\x01\x02") + bytearray((len(name) + 1, 0x09)) + name
        )


# test it
if __name__ == '__main__':
    # blue_led = Pin(2, Pin.OUT)
    rcv_trn_led = Pin(0, Pin.OUT, Pin.PULL_UP) # 1-internal led
    ble = BLE("ESP32", rcv_trn_led) 

# how to use it:
# Hi, I am developing a code and it is like that at the moment. To use it, just have a serial communication application via BLE on the smartphone (I use the Serial Bluetooth Terminal).

# Serial Bluetooth Terminal: https://play.google.com/store/apps/deta ... l&hl=pt_BR

# Settings (App):
# 1. Terminal: Font size(14), Font style(Normal), Charset(UTF-8), Display mode(Text), Auto scroll(on),
# Show connection messages(on), Show timestamps(on), Timestamp(I left default), Buffer size(10 kB).
# 2. Receive: Newline(LF).
# 3. Send: Newline(LF), Edit mode(Text), Line delay(0 ms), Character delay(0 ms), Local echo(on), Clear input(on).
# 4. Misc(I left default).

# MCU: ESP-WROOM-32 (ESP32D0WDQ6)
# Firmware: MicroPython v1.12 (for ESP32 with IDF4, 2019.12.20) https://micropython.org/resources/firmw ... -v1.12.bin
# IDE: Thonny Python IDE
# SO: Windows 10 Home Single Language 2004

# Use ble.send ("<message>") to send messages to the smartphone.
# Messages sent to ESP32 are displayed on the terminal.
# Blinking blue LED indicates that BLE communication is available
