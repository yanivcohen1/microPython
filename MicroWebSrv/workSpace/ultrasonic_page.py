from microWebSrv.microWebSrv import MicroWebSrv
import json
# from time import sleep
from _thread import allocate_lock  # ,start_new_thread
from machine import Pin, ADC, time_pulse_us, SoftI2C
from events_data_page import _chatLock , routeHandlers
from   _thread     import start_new_thread
from time import sleep
try:
    from time import sleep_us
except:
    from machine import sleep_us
try:
    # import user_lib.SSD1315_OLED_DISP as ssd1306
    import user_lib.sh1106 as ssd1306
except:
    from machine import ssd1306

# ESP32 Pin assignment 
i2c = SoftI2C(scl=Pin(22), sda=Pin(21))
oled_width = 128
oled_height = 64
oled = ssd1306.SH1106_I2C(oled_width, oled_height, i2c) # SSD1306_I2C

# display in 4 rows
oled.sleep(False)
oled.fill(0)

# oled.text('Welcome', 0, 0)
# oled.text('OLED Display', 0, 10)
# oled.text('how2electronics', 0, 20)
# oled.text('Makerfabs', 0, 30)
# oled.show()

global _chatWebSockets
_chatWebSockets = [ ]

led = Pin(32, Pin.OUT)
echoPin = Pin(35, Pin.IN)
trigPin = Pin(33, Pin.OUT)
# led.value(1)
led.off()

print('ultrasonic page load')
sliderIn = 25
ledOn = False
alarmIs = 'OFF'
curt_slider = 0
# ----------------------------------------------------------------------------

def WSJoinChat(webSocket, addr):
    webSocket.RecvTextCallback = OnWSChatTextMsg
    # webSocket.RecvBinaryCallback = _recvBinaryCallback
    webSocket.ClosedCallback = OnWSChatClosed
    # addr = webSocket.Request.UserAddress
    with _chatLock:
        print('<%s:%s HAS JOINED THE CHAT>' % addr)
        send = {}
        send[SendData.slider] = str(sliderIn)
        webSocket.SendText(json.dumps(send))
        _chatWebSockets.append(webSocket)
        print('<WELCOME %s:%s>' % addr)
        oldDisplay()
    # For looping see swTimerServer.py
    try:
	    start_new_thread(cb_timer, (1, webSocket))
    except:
        print ("Error: unable to start thread")

def OnWSChatClosed(webSocket) :
	print("WS CLOSED")
    
# for sending in timer the results in time period
def cb_timer(delay_sec, websocket):
    while True: 
        sleep(delay_sec)
        global curt_slider
        global alarmIs
        curt_slider = calcDistance()
        with _chatLock:
            for ws in _chatWebSockets:
                send = {}
                send[SendData.distance] = str(curt_slider)
                ws.SendText(json.dumps(send))
                print('ws sending distance: ', curt_slider)
                oldDisplay()
        global ledOn
        if curt_slider > sliderIn and ledOn :
            with _chatLock:
                for ws in _chatWebSockets:
                    send = {}
                    send[SendData.led] = str(False)
                    ws.SendText(json.dumps(send))
                    print('ws sending led: ', False)
                    ledOn = False
                    led.off()
                    alarmIs = 'OFF'
                    oldDisplay()
        elif curt_slider <= sliderIn and not ledOn :
            with _chatLock:
                for ws in _chatWebSockets:
                    send = {}
                    send[SendData.led] = str(True)
                    ws.SendText(json.dumps(send))
                    print('ws sending led: ', True)
                    ledOn = True
                    led.on()
                    alarmIs = 'ON'
                    oldDisplay()
        
def OnWSChatTextMsg(webSocket, msg):
    recv = json.loads(msg)
    if RecData.slider in recv:
        global sliderIn
        sliderIn = int(recv[RecData.slider])
        print('slider set to is: ', recv[RecData.slider])
        with _chatLock:
            for ws in _chatWebSockets:
                send = {}
                send[SendData.slider] = str(sliderIn)
                ws.SendText(json.dumps(send))
                oldDisplay()

#https://create.arduino.cc/projecthub/abdularbi17/ultrasonic-sensor-hc-sr04-with-arduino-tutorial-327ff6
def calcDistance():
    distance = 0
    for i in range(10):
        trigPin.off() # digitalWrite(trigPin, LOW);
        sleep_us(2) # delayMicroseconds(2);
        # Sets the trigPin on HIGH state for 10 micro seconds
        trigPin.on() # digitalWrite(trigPin, HIGH);
        sleep_us(10) # delayMicroseconds(10);
        trigPin.off() # digitalWrite(trigPin, LOW);
        # Reads the echoPin, returns the sound wave travel time in microseconds
        # calculate how mach time is on (time to go forword and back)
        duration = time_pulse_us(echoPin, 1) # pulseIn(echoPin, HIGH);
        # Calculating the distance(cm) - duration(µs) * 0.034cm/µs (speed of sound) / 2(distance is duble forword and backword)
        distance += duration*0.034/2
    return int(distance / 10) # distace in (cm)

def oldDisplay():
    oled.fill(0)
    oled.text('Distance System!', 0, 0) # 16 lines
    oled.text('Distance is: ' + str(curt_slider), 0, 10)
    oled.text('Distance Set ' + str(sliderIn), 0, 20)
    oled.text('Alarm is ' + alarmIs, 0, 30)
    oled.show()
# =============================================================================

class SendData :
    distance = 'distance'
    led = 'led'
    slider = 'slider'

class RecData:
   slider = 'slider' 

