from microWebSrv.microWebSrv import MicroWebSrv
import json
# from time import sleep
from _thread import allocate_lock  # ,start_new_thread
from machine import Pin, ADC, time_pulse_us
from events_data_page import _chatLock , routeHandlers
from   _thread     import start_new_thread
from time import sleep

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
        curt_slider = calcDistance()
        with _chatLock:
            for ws in _chatWebSockets:
                send = {}
                send[SendData.distance] = str(curt_slider)
                ws.SendText(json.dumps(send))
                print('ws sending temp: ', curt_slider)
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
        elif curt_slider <= sliderIn and not ledOn :
            with _chatLock:
                for ws in _chatWebSockets:
                    send = {}
                    send[SendData.led] = str(True)
                    ws.SendText(json.dumps(send))
                    print('ws sending led: ', True)
                    ledOn = True
                    led.on()

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

#https://create.arduino.cc/projecthub/abdularbi17/ultrasonic-sensor-hc-sr04-with-arduino-tutorial-327ff6
def calcDistance():
    distance = 0
    for i in range(10):
        trigPin.off() # digitalWrite(trigPin, LOW);
        sleep(2/1000000) # delayMicroseconds(2);
        # Sets the trigPin on HIGH state for 10 micro seconds
        trigPin.on() # digitalWrite(trigPin, HIGH);
        sleep(10/1000000) # delayMicroseconds(10);
        trigPin.off() # digitalWrite(trigPin, LOW);
        # Reads the echoPin, returns the sound wave travel time in microseconds
        # calculate how mach time is on (time to go forword and back)
        duration = time_pulse_us(echoPin, 1) # pulseIn(echoPin, HIGH);
        # Calculating the distance(cm) - duration(µs) * 0.034cm/µs (speed of sound) / 2(distance is duble forword and backword)
        distance += duration*0.034/2
    return int(distance / 10) # distace in (cm)
# =============================================================================

class SendData :
    distance = 'distance'
    led = 'led'
    slider = 'slider'

class RecData:
   slider = 'slider' 

