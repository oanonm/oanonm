import socket
import threading
import select
import sys

targetHost = 'www.yahoo.com'
targetPort = 80
f = open('data')
x = f.read().split(':')
f.close()
targetHost = x[0]
targetPort = int(x[1])

terminateAll = False

class ClientThread(threading.Thread):
	def __init__(self, clientSocket, targetHost, targetPort):
		threading.Thread.__init__(self)
		self.__clientSocket = clientSocket
		self.__targetHost = targetHost
		self.__targetPort = targetPort

	def run(self):
		print "Client Thread started"

		self.__clientSocket.setblocking(0)

		targetHostSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		targetHostSocket.connect((self.__targetHost, self.__targetPort))
		targetHostSocket.setblocking(0)

		clientData = ""
		targetHostData = ""
		terminate = False
		while not terminate and not terminateAll:
			inputs = [self.__clientSocket, targetHostSocket]
			outputs = []

			if len(clientData) > 0:
				outputs.append(self.__clientSocket)

			if len(targetHostData) > 0:
				outputs.append(targetHostSocket)

			try:
				inputsReady, outputsReady, errorsReady = select.select(inputs, outputs, [], 1.0)
			except Exception, e:
				print e
				break

			for inp in inputsReady:
				if inp == self.__clientSocket:
					try:
						data = self.__clientSocket.recv(4096)
					except Exception, e:
						print e

					if data != None:
						if len(data) > 0:
							targetHostData += data
						else:
							terminate = True
				elif inp == targetHostSocket:
					try:
						data = targetHostSocket.recv(4096)
					except Exception, e:
						print e

					if data != None:
						if len(data) > 0:
							clientData += data
						else:
							terminate = True

			for out in outputsReady:
				if out == self.__clientSocket and len(clientData) > 0:
					bytesWritten = self.__clientSocket.send(clientData)
					if bytesWritten > 0:
						clientData = clientData[bytesWritten:]
				elif out == targetHostSocket and len(targetHostData) > 0:
					bytesWritten = targetHostSocket.send(targetHostData)
					if bytesWritten > 0:
						targetHostData = targetHostData[bytesWritten:]

		self.__clientSocket.close()
		targetHostSocket.close()
		print "ClienThread terminating"

if __name__ == '__main__':
	localHost = ''
	localPort = int(sys.argv[1])
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	serverSocket.bind((localHost, localPort))
	serverSocket.listen(5)
	print "Waiting for client..."
	while True:
		try:
			clientSocket, address = serverSocket.accept()
		except KeyboardInterrupt:
			print "\nTerminating..."
			terminateAll = True
			break
		ClientThread(clientSocket, targetHost, targetPort).start()

	serverSocket.close()