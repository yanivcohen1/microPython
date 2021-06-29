from microWebSrv.microWebSrv import MicroWebSrv
import json
# from time import sleep
from _thread import allocate_lock  # ,start_new_thread
from machine import Pin
from events_data_page import _chatLock
from   _thread     import start_new_thread
from time import sleep

global _chatWebSockets
_chatWebSockets = [ ]

led = Pin(2, Pin.OUT)
btn = Pin(0, Pin.IN)
# led.value(1)
led.on()  # the opesit on is off and off in on

print('contiuse_data page load')

def btn_change(pin):
    cur_btn = btn.value()
    with _chatLock:
        for ws in _chatWebSockets:
            send = {}
            send['btn'] = str(cur_btn == 1)
            ws.SendText(json.dumps(send))
            print('ws sending: ', cur_btn)

    if cur_btn == 1:  # btn is not press
        print('btn not pressed')
    else:
        print('btn pressed')

btn.irq(btn_change)

# ----------------------------------------------------------------------------

def WSJoinChat(webSocket, addr):
    webSocket.RecvTextCallback = OnWSChatTextMsg
    # webSocket.RecvBinaryCallback = _recvBinaryCallback
    webSocket.ClosedCallback = OnWSChatClosed
    # addr = webSocket.Request.UserAddress
    with _chatLock:
        for ws in _chatWebSockets:
            print('<%s:%s HAS JOINED THE CHAT>' % addr)
        _chatWebSockets.append(webSocket)
        print('<WELCOME %s:%s>' % addr)
    # For looping see swTimerServer.py
    try:
	    start_new_thread(cb_timer, (3, webSocket))
    except:
        print ("Error: unable to start thread")
	# OR Using the HW Timer
	# from machine import Onewire, RTC, Timer
	# cb = lambda timer: cb_timer(timer, webSocket)
	# Init and start timer to poll evry 3 sec temperature sensor
	# tm = Timer(0)
	# tm.init(period=3000, callback=cb)

# for sending in timer the results in time period
def cb_timer(delay_sec, websocket):
    while True: 
        sleep(delay_sec)
        #Read data from sensors and Store in dict
        #Convert dictionary data to JSON and send
        curt_btn = btn.value()
        with _chatLock:
            for ws in _chatWebSockets:
                send = {}
                send['btn'] = str(curt_btn == 1)
                ws.SendText(json.dumps(send))
                print('ws sending: ', curt_btn)

def OnWSChatTextMsg(webSocket, msg):
    with _chatLock:
        for ws in _chatWebSockets:
            pass
            # ws.SendText('<%s:%s> %s' % (addr[0], addr[1], msg))

def OnWSChatClosed(webSocket):
    with _chatLock:
        if webSocket in _chatWebSockets:
            _chatWebSockets.remove(webSocket)
            for ws in _chatWebSockets:
                ws.SendText('DISCONNECT')

# ============================================================================
