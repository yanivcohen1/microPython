from microWebSrv import MicroWebSrv
import json
# from time import sleep
from _thread import allocate_lock  # ,start_new_thread
from machine import Pin
import main_start_ws

led = Pin(1, Pin.OUT)
btn = Pin(0, Pin.IN)

# led.value(1)
led.on()  # the opesit on is off and off in on

def btn_change(pin):
    cur_btn = btn()
    with main_start_ws._chatLock:
        for ws in main_start_ws._chatWebSockets:
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
        with main_start_ws._chatLock:
            for ws in main_start_ws._chatWebSockets:
                send = {}
                send['led'] = str(args['status'] == 'false')
                ws.SendText(json.dumps(send))
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
    with main_start_ws._chatLock:
        for ws in main_start_ws._chatWebSockets:
            print('<%s:%s HAS JOINED THE CHAT>' % addr)
        main_start_ws._chatWebSockets.append(webSocket)
        print('<WELCOME %s:%s>' % addr)

def OnWSChatTextMsg(webSocket, msg):
    addr = _calcAddr(webSocket)  # webSocket.Request.UserAddress
    with main_start_ws._chatLock:
        for ws in main_start_ws._chatWebSockets:
            ws.SendText('<%s:%s> %s' % (addr[0], addr[1], msg))

def OnWSChatClosed(webSocket):
    addr = _calcAddr(webSocket)  # webSocket.Request.UserAddress
    with main_start_ws._chatLock:
        if webSocket in main_start_ws._chatWebSockets:
            main_start_ws._chatWebSockets.remove(webSocket)
            for ws in main_start_ws._chatWebSockets:
                ws.SendText('<%s:%s HAS LEFT THE CHAT>' % addr)

def _calcAddr(webSocket):
    addr = str(webSocket._socket)
    x = addr.find("raddr=('") + 8
    y = addr[x:]
    z = y.find("'")
    host = addr[x:x+z]
    y = addr[x+z:]
    z = y.find(")")
    port = y[3:z]
    return [host, port]

# ============================================================================
