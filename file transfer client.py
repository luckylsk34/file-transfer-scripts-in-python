import socket
import time
import os

def mrecv(n):
	return (clientsocket.recv(n)).decode('ascii')
"""def recvint():
	return (int(clientsocket.recv(51)).decode('ascii'))
"""
clientsocket = socket.socket()

host = '10.102.46.' + input('host ip : 10.102.46.')
port = 9999

clientsocket.connect((host, port))
try:
	print('server:', mrecv(1024))
except Exception as error:
	print(error)
	exit()

print('connected to', host, 'on', port)

"""length = recvint()
filename = mrecv(length)
"""
filename = input('filename :')

with open(filename, 'wb') as f:
	print('starting file transfer\nrecieving file...')
	c1 = time.time()
	while True:
		data = clientsocket.recv(4096)
		if not data:
			break
		f.write(data)
c2 = time.time()
size = ((os.stat(filename)).st_size)/1024**2
f.close()
print('file transfer complete')

print('\nStats\nTime taken :%0.2f' % (c2-c1))
print('size :%0.2f' % size, 'MB')
print('Speed :%0.3f' % (size/(c2-c1)), 'MBps')