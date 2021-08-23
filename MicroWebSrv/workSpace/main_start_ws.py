
from time import sleep
from microWebSrv.microWebSrv import MicroWebSrv
from microWebSrv.microWebSocket import MicroWebSocket
# from time import sleep
# from   _thread   import allocate_lock ,start_new_thread
# for ultrasonic page auto load
# from ultrasonic_page import WSJoin as ultrasonicWSJoin 	
# ultrasonicWSJoin(None, None) # for page auto load	
import user_lib.settings as settings
from events_data_page import WSJoinChat as MyWSJoinChat
from events_data_page import routeHandlers
from machine import RTC
simulation = False
try:
	import ntptime
except:
	simulation = True
# update clock from internet
# synchronize with ntp
# need to be connected to wifi
rtc = RTC()
if not simulation:
	i = 0
	while i < 7:
		try:
			ntptime.settime() # set the rtc datetime from the remote server	
			year, monte, day, houre1, houre, mimite, secend, n = rtc.datetime()
			i = 8
		except:
			print("main waiting for the internet")
			sleep(10)
			i += 1

if year == 2000:
	print("error connect to ntptime remote server")
# add time up to log
log = "Up time: " +  str(day) + '-' + str(monte) + ' ' + str(houre+3) \
		    + ':' + str(mimite) + ':' + str(secend) # 2018-03-29 10:26:23
if simulation:
	log = rtc.datetime()
print(log)
settings.appendLineToLogFile(log)

# read log file
# lines = settings.readLinesFromLogFile()
# for line in lines:
#     print(line)

global _chatWebSockets
_chatWebSockets = [ ]

# test web socket [/wstest.html]
def _acceptWebSocketCallback(webSocket: MicroWebSocket, httpClient: MicroWebSrv._client)-> None:
	print('Example WebSocket accepted:')
	print('   - User   : %s:%s' % (httpClient.GetAddr()[0], httpClient.GetAddr()[1]))
	print('   - Path   : %s'    % httpClient.GetRequestTotalPath())
	# print('   - Origin : %s'    % webSocket.Request.Origin)
	if httpClient.GetRequestTotalPath().lower() == '/wschat' :
	    from tester.chat_page import WSJoinChat		
	    WSJoinChat(webSocket, httpClient.GetAddr())
	elif httpClient.GetRequestTotalPath().lower() == '/wstest' :
		webSocket.RecvTextCallback   = _recvTextCallback
		webSocket.RecvBinaryCallback = _recvBinaryCallback
		webSocket.ClosedCallback 	 = _closedCallback
	elif httpClient.GetRequestTotalPath().lower() == '/events_data_page' :
		MyWSJoinChat(webSocket, httpClient.GetAddr())
	elif httpClient.GetRequestTotalPath().lower() == '/contineuse-data-read' :
		from contiuse_data_page import WSJoinChat as ContiuseWSJoinChat
		ContiuseWSJoinChat(webSocket, httpClient.GetAddr())
	elif httpClient.GetRequestTotalPath().lower() == '/boiler' :
		from boiler_page import WSJoinChat as BoilerWSJoinChat
		BoilerWSJoinChat(webSocket, httpClient.GetAddr())
	elif httpClient.GetRequestTotalPath().lower() == '/ultrasonic_page' :
		from ultrasonic_page import WSJoin as ultrasonicWSJoin
		ultrasonicWSJoin(webSocket, httpClient.GetAddr())     
	# For looping see swTimerServer.py
	# _thread.start_new_thread(cb_timer, (3, webSocket)
	# OR Using the HW Timer
	# from machine import Onewire, RTC, Timer
	# cb = lambda timer: cb_timer(timer, webSocket)
	# Init and start timer to poll evry 3 sec temperature sensor
	# tm = Timer(0)
	# tm.init(period=3000, callback=cb)

	# for sending in timer the results in time period
	# def cb_timer(delay_sec, websocket): 
	# time.sleep(delay_sec)
    # Read data from sensors and Store in dict
    # Convert dictionary data to JSON and send
    # websocket.SendText(json.dumps(dict))

def _recvTextCallback(webSocket: MicroWebSocket, msg: str) -> None :
	print("WS RECV TEXT : %s" % msg)
	webSocket.SendText("Reply for %s" % msg)

def _recvBinaryCallback(webSocket, data) :
	print("WS RECV DATA : %s" % data)

def _closedCallback(webSocket) :
	print("WS CLOSED")

# ----------------------------------------------------------------------------


# routeHandlers = [
#	( "/test",	"GET",	_httpHandlerTestGet ),
#	( "/test",	"POST",	_httpHandlerTestPost )
# ]

# ============================================================================

srv = MicroWebSrv(webPath='www/', routeHandlers=routeHandlers) # port=<portNumber> default is 80
srv.MaxWebSocketRecvLen     = 500
srv.WebSocketThreaded		= True
srv.AcceptWebSocketCallback = _acceptWebSocketCallback
print('running WebServer')
# control+C press
srv.Start(threaded=False) 
# try : # srv.Start(threaded=True)
#     while True :
#         sleep(2)
# except KeyboardInterrupt : # control+C press
#     pass
print('stopping server and cleanup')
srv.Stop()
# ----------------------------------------------------------------------------
