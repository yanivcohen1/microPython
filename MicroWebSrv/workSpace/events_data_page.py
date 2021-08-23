from microWebSrv.microWebSrv import MicroWebSrv
import json
from time import sleep
from _thread import allocate_lock, start_new_thread
# C:\Users\yaniv\AppData\Local\Programs\Thonny\Lib\site-packages\thonny\plugins\micropython\api_stubs
from machine import Pin
import user_lib.settings as settings
import user_lib.webLiveTest as webLiveTest
from machine import Pin, ADC, SoftI2C, Timer, I2C, WDT, PWM, Signal
simulation = False
try:
    from time import sleep_us, ticks_ms, ticks_diff
    # import user_lib.sh1106 as ssd1306
except:
    from machine import sleep_us, ticks_ms, ticks_diff
    simulation = True 
    # from machine import ssd1306

timer0 = Timer(0)
bazzer = Signal(Pin(27, Pin.OUT, value=0), invert=False) # 
relay = Signal(Pin(13, Pin.OUT, value=1), invert=True) # 

routeHandlers = []
#	( "/test",	"GET",	_httpHandlerTestGet ),
#	( "/test",	"POST",	_httpHandlerTestPost )
# ]

led = Pin(5, Pin.OUT, value=1) # 1, Pin.PULL_UP
# btn = Pin(0, Pin.IN) # Pin.PULL_UP
# led.value(1)
# led.off()  # the opesit on is off and off in on

print('events_data page load')

global _chatWebSockets
_chatWebSockets = [ ]

global _chatLock
_chatLock = allocate_lock()

global res

def cb_timer(delay_sec, websocket):
    while True:
        # global wdt_last
        sleep(delay_sec)
        fun_timer(None, None)
        # wtd_now = ticks_ms()
        # print('wtd: ', wtd_now - wdt_last)
        #wdt_last = wtd_now
        #with _chatLock:
        # need wochdog
        # print('auarer lock')
        

def fun_timer(delay, websocket):
    wdt = WDT(timeout=60000) # enable the wachdog with a timeout of 20s (1s is the minimum)
    wdt.feed() # need to call this wachdog fun minimum evry 20s or the bord will restart itself
    from machine import RTC
    # update clock from internet
    rtc = RTC()
    year, monte, day, houre1, houre, mimite, secend, n = rtc.datetime()
    # add time up to log
    log = str(day) + '-' + str(monte) + ' ' + str(houre+3) \
                + ':' + str(mimite) + ':' + str(secend) # 2018-03-29 10:26:23
    if not webLiveTest.liveTest(): # fail test
        bazzer.on()
        sleep(20)
        if not webLiveTest.liveTest(): # still error
            relay.on()
            sleep(5)
            relay.off()
            print("reset wifi")
            print("reset time: " + log)
            settings.appendLineToLogFile("reset time: " + log)
    else: print("pass live test: " + log)
        
esp32NoSpram = False
try:
    import ubinascii
    import machine
    device_unique_id = ubinascii.hexlify(machine.unique_id()).decode('utf-8')
    if device_unique_id == '2462abe768e4':
        esp32NoSpram = True
    else: esp32NoSpram = False
except:
    pass

if simulation and esp32NoSpram:
    start_new_thread(cb_timer, (1, None))
elif not simulation and esp32NoSpram: # for WH Timer - if not simulation:
    cb = lambda timer: fun_timer(timer, None)
    timer0.init(period=30000, callback=cb) # 30sec timer


# ----------------------------------------------------------------------------

# test get query parameters [/send?name=yaniv&last=cohen]
@MicroWebSrv.route('/led')
def _httpHandlerEditWithArgs(httpClient, httpResponse):
    args = httpClient.GetRequestQueryParams()
    # print('QueryParams', args)
    content = ""
    if 'status' in args:
        if args['status'] == 'false':
            led.on()
        else:
            led.off()
        print('led is: ', args['status'])
        with _chatLock:
            for ws in _chatWebSockets:
                send = {}
                send['led'] = str(args['status'] == 'false')
                try: ws.SendText(json.dumps(send))
                except: pass
                # ws.SendText('{"led": "'+ str(args['status'] == 'false')+'"}')
                print('ws sending: ', args['status'] == 'false')
    httpResponse.WriteResponseOk(headers=None,
                                 contentType="text/html",
                                 contentCharset="UTF-8",
                                 content=content)

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

def OnWSChatTextMsg(webSocket, msg):
    print('msg is: ', msg)
    recv = json.loads(msg)
    if 'msg' in recv:
        msgIn = recv['msg']
        print('msg is: ', msgIn)
        global res
        res = None
        exec(msgIn)
        if res != None:
            print('res is: ', res)
            send = {}
            send['res'] = str(res)
            try: webSocket.SendText(json.dumps(send))
            except: pass
    elif 'log' in recv:
        logIn = recv['log']
        print('ws sending log')
        lines = settings.readLinesFromLogFile()
        lines.reverse()
        send = {}
        send['log'] = lines
        try: webSocket.SendText(json.dumps(send))
        except: pass

def OnWSChatClosed(webSocket) :
    _chatWebSockets.remove(webSocket)
    print("WS CLOSED")
# ============================================================================

def btn_change(pin):
    cur_btn = 1 # btn()
    with _chatLock:
        for ws in _chatWebSockets:
            send = {}
            send['btn'] = str(cur_btn == 1)
            try: ws.SendText(json.dumps(send))
            except: pass
            print('ws sending: ', cur_btn)

    if cur_btn == 1:  # btn is not press
        print('btn not pressed')
    else:
        print('btn pressed')

# btn.irq(btn_change)
