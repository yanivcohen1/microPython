from microWebSrv import MicroWebSrv
import json
# import time import sleep
from   _thread   import allocate_lock # ,start_new_thread

@MicroWebSrv.route('/test-redir')
def _httpHandlerTestGet(httpClient, httpResponse):
	httpResponse.WriteResponseRedirect('/test.pdf')
# ----------------------------------------------------------------------------

# test get page [/test-post]
@MicroWebSrv.route('/test-post')
def _httpHandlerTestGet(httpClient, httpResponse):
	content = """\
	<!DOCTYPE html>
	<html lang=en>
        <head>
        	<meta charset="UTF-8" />
            <title>TEST GET</title>
        </head>
        <body>
            <h1>TEST GET</h1>
            Client IP address = %s
            <br />
			<form action="/test-post" method="post" accept-charset="ISO-8859-1">
				First name: <input type="text" name="firstname"><br />
				Last name: <input type="text" name="lastname"><br />
				<input type="submit" value="Submit">
			</form>
        </body>
    </html>
	""" % httpClient.GetIPAddr()
	httpResponse.WriteResponseOk(headers=None,
								  contentType="text/html",
								  contentCharset="UTF-8",
								  content=content)
# ----------------------------------------------------------------------------

# test post data [/test-post]
@MicroWebSrv.route('/test-post', 'POST')
def _httpHandlerTestPost(httpClient, httpResponse):
	formData = httpClient.ReadRequestPostedFormData()
	firstname = formData["firstname"]
	lastname = formData["lastname"]
	content = """\
	<!DOCTYPE html>
	<html lang=en>
		<head>
			<meta charset="UTF-8" />
            <title>TEST POST</title>
        </head>
        <body>
            <h1>TEST POST</h1>
            Firstname = %s<br />
            Lastname = %s<br />
        </body>
    </html>
	""" % (MicroWebSrv.HTMLEscape(firstname),
		    MicroWebSrv.HTMLEscape(lastname))
	httpResponse.WriteResponseOk(headers=None,
								  contentType="text/html",
								  contentCharset="UTF-8",
								  content=content)
# ----------------------------------------------------------------------------

# test get query parameters [/send?name=yaniv&last=cohen]
@MicroWebSrv.route('/send')
def _httpHandlerEditWithArgs(httpClient, httpResponse):
	args = httpClient.GetRequestQueryParams()
	# print('QueryParams', args)
	content = """\
	<!DOCTYPE html>
	<html lang=en>
        <head>
        	<meta charset="UTF-8" />
            <title>TEST EDIT</title>
        </head>
        <body>
	"""
	content += "<h1>EDIT item with {} query arguments</h1>"\
		.format(len(args))

	if 'name' in args:
		content += "<p>name = {}</p>".format(args['name'])

	# if 'last' in args :
	#	content += "<p>last name = {}</p>".format(args['last'])

	for key in args:
		if key != "name": content += "<p>{key} = {val}</p>".format(
		    key=key, val=args[key])

	content += """
        </body>
    </html>
	"""
	httpResponse.WriteResponseOk(headers=None,
								  contentType="text/html",
								  contentCharset="UTF-8",
								  content=content)
# ----------------------------------------------------------------------------

# test path variable [see comments]
# <IP>/edit/123           ->   args['index']=123
@MicroWebSrv.route('/edit/<index>')
# <IP>/edit/123/abc/bar   ->   args['index']=123  args['foo']='bar'
@MicroWebSrv.route('/edit/<index>/abc/<foo>')
# <IP>/edit               ->   args={}
@MicroWebSrv.route('/edit')
def _httpHandlerEditWithArgs(httpClient, httpResponse, args={}):
	content = """\
	<!DOCTYPE html>
	<html lang=en>
        <head>
        	<meta charset="UTF-8" />
            <title>TEST EDIT</title>
        </head>
        <body>
	"""
	content += "<h1>EDIT item with {} variable arguments</h1>"\
		.format(len(args))

	if 'index' in args:
		content += "<p>index = {}</p>".format(args['index'])

	if 'foo' in args:
		content += "<p>foo = {}</p>".format(args['foo'])

	content += """
        </body>
    </html>
	"""
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
	if httpClient.GetRequestTotalPath().lower() == '/wschat' :
	    WSJoinChat(webSocket, httpClient.GetAddr()[0])
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
            ws.SendText('<%s HAS JOINED THE CHAT>' % addr)
        _chatWebSockets.append(webSocket)
        webSocket.SendText('<WELCOME %s>' % addr)

def OnWSChatTextMsg(webSocket, msg) :
    addr = _calcAddr(webSocket) # webSocket.Request.UserAddress
    with _chatLock :
        for ws in _chatWebSockets :
            ws.SendText('<%s> %s' % (addr, msg))

def OnWSChatClosed(webSocket) :
    addr =  _calcAddr(webSocket) # webSocket.Request.UserAddress
    with _chatLock :
        if webSocket in _chatWebSockets :
            _chatWebSockets.remove(webSocket)
            for ws in _chatWebSockets :
                ws.SendText('<%s HAS LEFT THE CHAT>' % addr)

def _calcAddr(webSocket):
	addr= str(webSocket._socket)
	x = addr.find("raddr=('") + 8
	y= addr[x:]
	z = y.find("'")
	addrs=addr[x:x+z]
	return addrs
# ============================================================================
# ============================================================================
# ============================================================================

srv = MicroWebSrv(webPath='www/')
srv.MaxWebSocketRecvLen     = 256
srv.WebSocketThreaded		= False
srv.AcceptWebSocketCallback = _acceptWebSocketCallback
print('running WebServer')
srv.Start(threaded=False)
# ----------------------------------------------------------------------------
