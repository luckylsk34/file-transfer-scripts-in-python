import socket
import time
from os import sys

def msend(message):
	clientsocket.send(message.encode('ascii'))

serversocket = socket.socket() #create a socket object
host = socket.gethostname()
port = 9999 #port for the socket

serversocket.bind((host, port))

serversocket.listen(5)

while True:
	clientsocket, addr = serversocket.accept()
	try:
		msend('client accepted')
	except Exception as error:
		print(error)
		exit()

	print("Got a connection from ", str(addr))

	filename = input("file to send: ")
	"""sendint(sys.getsizeof(filename))
	msend(filename)
"""
	f = open(filename, 'rb')
	l = f.read(4096)
	while l:
		clientsocket.send(l)
		l = f.read(4096)

	f.close()

	print('Done sending')
	clientsocket.close()
	print('Client connection closed')
	if input('exit? y or n : ') == 'y':
		exit()