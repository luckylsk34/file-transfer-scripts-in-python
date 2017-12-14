import socket
import time
import os

def size_(a):
	return len(a)

def mrecv(n):
	return (clientsocket.recv(n)).decode('ascii')

clientsocket = socket.socket()

host = input('host ip : ')
port = 9999

clientsocket.connect((host, port))
try:
	print('server:', mrecv(1024))
except Exception as error:
	print(error)
	exit()

print('connected to', host, 'on', port)
print('waiting for filename', end = '\r')
lv2size = (clientsocket.recv(1)).decode('ascii')
lv1size = (clientsocket.recv(int(lv2size))).decode('ascii')
filename = (clientsocket.recv(int(lv1size))).decode('ascii')
filename = '1'+filename
print('filename:', filename)

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