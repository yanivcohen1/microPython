from microbit import uart, sleep

uart.init(115200)
print('starting..')

while True:
    print("serial write msg")
    while not uart.any():
        sleep(100)
    sleep(2000)  # delay to wait to end typeping
    msg = uart.readline()
    print('receive: ' + str(msg, 'ascii'))
