from microbit import *
import radio

radio.config(group=132)
radio.on()

def get_message():
    while True:
        try:
            msg = radio.receive_bytes()
            if msg is not None:
                if len(msg) >= 13 and msg[3] == 2:
                    lstr = msg[12]  # length byte
                    text = str(msg[13:13+lstr], 'ascii')
                    return text

        except Exception as e:  # reset radio on error
            print("reset %s" % str(e))
            radio.off()
            radio.on()

while True:
    print("waiting...")
    display.show('?')

    m = get_message()
    print('got message:', m)
    display.scroll(m)
