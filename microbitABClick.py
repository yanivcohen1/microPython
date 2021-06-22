from microbit import *
import emoji
# import ujson

uart.init(115200)
print("starting..")
index = 0
while True:
    if not uart.any():
        if button_a.is_pressed() and button_b.is_pressed():
            display.scroll("AB")
            sleep(100)
            #  break
        display.show(emoji.HAPPY)
        if accelerometer.was_gesture("shake"):
            display.show(emoji.ANGRY)
            sleep(1000)
            print("angry")
        elif button_a.was_pressed():
            display.show(emoji.HEART)
            print("a1")
            sleep(1000)
        elif button_b.was_pressed():
            display.show(emoji.HOUSE)
            print("b1")
            sleep(1000)
            json1 = {
                "command" : "Danilo1",
                "orderId" : +index,
                "quantity" : 151,
                "status" : "CREATED",
            }
            #  json_str = ujson.dumps(json1)
            #  user_json = ujson.loads(json_str)
            #  print("print command:" + str(user_json["command"]) +
            #        "; order:" + str(user_json["orderId"]))
        sleep(100)
    else:
        sleep(2000)  # delay to wait to end typeping
        msg = uart.readline()
        print("serial receive: " + str(msg, "ascii"))
