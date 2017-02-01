# my test server

import socket,sys
from func import *

PORT = int(sys.argv[1])

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind(('', PORT))
listen_socket.listen(1)
print 'Serving HTTP on port %s ...' % PORT
while True:
    client, client_address = listen_socket.accept()
    req = client.recv(8192)
    res = 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n'
    try:
        path = req.split(" ",3)[1][1:]
        data = path
        if (path.find("?") == -1 and path == '') or path.find('?') == 0:
            data = index(path)
        elif path.startswith("pg"):
            data = pg(path)
        res = res+data
    except Exception as e:
        res = res+str(e)#.replace('\n','<br>')
    client.sendall(res)
    client.close()