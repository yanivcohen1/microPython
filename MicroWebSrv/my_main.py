from microWebSrv import MicroWebSrv
import json
# from time import sleep
from   _thread   import allocate_lock # ,start_new_thread
from machine import Pin

led = Pin(1, Pin.OUT)
btn = Pin(0, Pin.IN)
## led.value(1)
led.on() # the opesit on is off and off in on

def btn_change(pin):
	cur_btn = btn()
	with _chatLock:
		for ws in _chatWebSockets:
			send = {}
			send['btn']= str(cur_btn == 1)
			ws.SendText(json.dumps(send))
			print('ws sending: ', cur_btn)
	if cur_btn == 1:  # btn is not press
		print('btn not pressed')
	else:
		print('btn pressed')

btn.irq(btn_change)

@MicroWebSrv.route('/test-redir')
def _httpHandlerTestGet(httpClient, httpResponse):
	httpResponse.WriteResponseRedirect('/my-main-page.html')
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
				send['led']= str(args['status'] == 'false')
				ws.SendText(json.dumps(send))
				# ws.SendText('{"led": "'+ str(args['status'] == 'false')+'"}')
				print('ws sending: ', args['status'] == 'false')

	httpResponse.WriteResponseOk(headers=None,
								  contentType="text/html",
								  contentCharset="UTF-8",
								  content=content)
# ----------------------------------------------------------------------------

# test web socket [/wstest.html]
def _acceptWebSocketCallback(webSocket, httpClient):
	print('Example WebSocket accepted:')
	print('   - User   : %s:%s' % (httpClient.GetAddr()[0], httpClient.GetAddr()[1]))
	print('   - Path   : %s'    % httpClient.GetRequestTotalPath())
	# print('   - Origin : %s'    % webSocket.Request.Origin)
	if True : # True for multi users
	    WSJoinChat(webSocket, httpClient.GetAddr())
	else :
		webSocket.RecvTextCallback   = _recvTextCallback
		webSocket.RecvBinaryCallback = _recvBinaryCallback
		webSocket.ClosedCallback 	 = _closedCallback
	# For looping see swTimerServer.py
	# _thread.start_new_thread(cb_timer, (3, webSocket)
	# OR Using the HW Timer
	# from machine import Onewire, RTC, Timer
	# cb = lambda timer: cb_timer(timer, webSocket)
	# Init and start timer to poll evry 3 sec temperature sensor
	# tm = Timer(0)
	# tm.init(period=3000, callback=cb)

def _recvTextCallback(webSocket, msg) :
	print("WS RECV TEXT : %s" % msg)
	webSocket.SendText("Reply for %s" % msg)

def _recvBinaryCallback(webSocket, data) :
	print("WS RECV DATA : %s" % data)

def _closedCallback(webSocket) :
	print("WS CLOSED")

# for sending in timer the results in time period
# def cb_timer(delay_sec, websocket): 
	# time.sleep(delay_sec)
    # Read data from sensors and Store in dict
    # Convert dictionary data to JSON and send
    # websocket.SendText(json.dumps(dict))
# ----------------------------------------------------------------------------

# routeHandlers = [
#	( "/test",	"GET",	_httpHandlerTestGet ),
#	( "/test",	"POST",	_httpHandlerTestPost )
# ]

# ============================================================================
# ============================================================================
# ============================================================================

global _chatWebSockets
_chatWebSockets = [ ]

global _chatLock
_chatLock = allocate_lock()

def WSJoinChat(webSocket, addr) :
    webSocket.RecvTextCallback = OnWSChatTextMsg
    webSocket.RecvBinaryCallback = _recvBinaryCallback
    webSocket.ClosedCallback      = OnWSChatClosed
    # addr = webSocket.Request.UserAddress
    with _chatLock :
        for ws in _chatWebSockets :
            print('<%s:%s HAS JOINED THE CHAT>' % addr)
        _chatWebSockets.append(webSocket)
        print('<WELCOME %s:%s>' % addr)

def OnWSChatTextMsg(webSocket, msg) :
    addr = _calcAddr(webSocket) # webSocket.Request.UserAddress
    with _chatLock :
        for ws in _chatWebSockets :
            ws.SendText('<%s:%s> %s' % (addr[0], addr[1], msg))

def OnWSChatClosed(webSocket) :
    addr =  _calcAddr(webSocket) # webSocket.Request.UserAddress
    with _chatLock :
        if webSocket in _chatWebSockets :
            _chatWebSockets.remove(webSocket)
            for ws in _chatWebSockets :
                ws.SendText('<%s:%s HAS LEFT THE CHAT>' % addr)

def _calcAddr(webSocket):
	addr= str(webSocket._socket)
	x = addr.find("raddr=('") + 8
	y= addr[x:]
	z = y.find("'")
	host=addr[x:x+z]
	y= addr[x+z:]
	z = y.find(")")
	port=y[3:z]
	return [host, port]

# ============================================================================
# ============================================================================
# ============================================================================

srv = MicroWebSrv(webPath='www/')
srv.MaxWebSocketRecvLen     = 256
srv.WebSocketThreaded		= True
srv.AcceptWebSocketCallback = _acceptWebSocketCallback
print('running WebServer')
srv.Start(threaded=False) # control+C press
""" try : # srv.Start(threaded=True)
    while True :
        sleep(2)
except KeyboardInterrupt : # control+C press
    pass """
# ----------------------------------------------------------------------------
