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
    # print('Testing...')
    # dataList = http_get('http://micropython.org/ks/test.html')
    dataList = http_get('http://api.mathjs.org/v4/?expr=2*(7-3)')
    for data in dataList:
        # print(data)
        if str(data).endswith('Via: 1.1 vegur\r\n\r\n8'): return True
    return False

if __name__ == '__main__':
     print('is test pass?: ',liveTest())