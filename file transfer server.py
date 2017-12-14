import socket
import time
from os import sys

def size_(a):
	return len(a)

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

	filename = input("file to send(with extension): ")
	lv1size = str(size_(filename))
	lv2size = str(size_(lv1size))
	
	clientsocket.send(lv2size.encode('ascii'))
	clientsocket.send(lv1size.encode('ascii'))
	clientsocket.send(filename.encode('ascii'))
	
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