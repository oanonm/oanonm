import socket,sys

HOST, PORT = '', int(sys.argv[1])

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print 'Serving HTTP on port %s ...' % PORT
while True:
    client, client_address = listen_socket.accept()
    req = client.recv(1024)
    res = 'HTTP/1.1 200 OK\r\n\r\n'
    try:
        path = req.split(" ")[1]
        res = res+path
    except Exception as e:
        res = res+str(e).replace('\n','<br>')
    client.sendall(res+data)
    client.close()