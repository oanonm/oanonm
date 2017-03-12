# my test server

import socket,sys
import os,urlparse
import argparse
import requests,time

PORT = int(sys.argv[1])

def index(path):
    with open('index.html') as f:
        return f.read();
    return '@'

def x(path):
    xt = path[2:].split('&')
    dt = dict()
    for xtz in xt:
        dtz = xtz.split('=')
        if len(dtz) == 2:
            dt[dtz[0]] = dtz[1]
    #return str(dt)
    f = dt['f']
    t = dt['t']
    #return t+f
    dx = {}
    x['from'] = f;
#'from':str(f),'type':'text','text':str(t)};
    return dx
    headers =  {'X-Viber-Auth-Token':os.environ['X-Viber-Auth-Token']}
    return headers
    res = requests.post('https://chatapi.viber.com/pa/post',data=data,headers=headers,json=data)
    return res.json();

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
        elif path.startswith("x"):
            data = x(path)
        res = res+data
    except Exception as e:
        res = res+str(e)#.replace('\n','<br>')
    client.sendall(res)
    client.close()