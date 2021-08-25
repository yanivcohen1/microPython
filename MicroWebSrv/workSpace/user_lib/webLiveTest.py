import socket

def http_get(url):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    retData = []
    while True:
        data = s.recv(100)
        if data:
            retData.append(str(data, 'utf8'))
            # print(str(data, 'utf8'), end='')
        else:
            break
    s.close()
    return retData

def liveTest():
    isPass = False
    # print('Testing...')
    try:
        dataList = http_get('http://api.mathjs.org/v4/?expr=2*(7-3)')
        isPass = True
    except:
        pass
    if not isPass:
        try:
            ntptime.settime() # set the rtc datetime from the remote server	
            isPass = True
        except:
            pass
    return isPass

if __name__ == '__main__':
     print('is test pass?: ',liveTest())