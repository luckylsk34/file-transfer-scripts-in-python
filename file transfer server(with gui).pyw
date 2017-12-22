import socket
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from threading import *
import time
from queue import *
import os

clientconnected = False
filename = ''

def size_(a):
	return len(a)

def wait():
	global clientconnected

	while not clientconnected:
		pass

class signal(QObject):
	sig = pyqtSignal()

class progresssignal(QObject):
	sig = pyqtSignal(int)

class CustomLabel(QLabel):

	def __init__(self, title, parent):
		super().__init__(title, parent)
		self.setAcceptDrops(True)

	def dragEnterEvent(self, e):
		e.accept()

	def dropEvent(self, e):
		global filename
		filename = (e.mimeData().text())[8:]

class serverWindow(QWidget):

	def __init__(self):
		super().__init__()

		self.initUI()

	def initUI(self):

		self.setFixedSize(400, 300)
		self.frame = self.frameGeometry()
		self.width = self.frame.width()
		self.height = self.height()
		self.setWindowTitle('server')
		self.setWindowIcon(QIcon('server.ico'))
		self.center()

		self.font = QFont()
		self.font.setFamily('yu gothic')
		self.font.setPointSize(16)
		self.font.setBold(True)

		self.lbl1 = QLabel('server started', self)
		self.lbl1.setFont(self.font)
		self.centerwidget(self.lbl1, 60)
		self.lbl2 = QLabel('waiting for connections...', self)
		self.centerwidget(self.lbl2, 180)
		self.lbl3 = CustomLabel('', self)
		self.lbl3.setPixmap(QPixmap('Drop-Files-Here-extra.png'))
		self.lbl3.resize(self.lbl3.sizeHint())
		self.lbl3.move((self.width-self.lbl3.frameGeometry().width())/2+5, 30)
		self.lbl3.hide()
		self.lbl4 = QLabel('sending the file.', self)
		self.centerwidget(self.lbl4, 180)
		self.lbl4.hide()
		self.lbl5 = QLabel('File sent', self)
		self.centerwidget(self.lbl5, 130)
		self.lbl5.hide()
		self.lblsig = signal()
		self.lblsig.sig.connect(self.showfoldermsgbox)

		self.isshown = False
		self.transfer = False

		self.msg = QMessageBox()
		self.msg.setIcon(QMessageBox.Information)
		self.msg.setText('Folders are not supported')
		self.msg.setWindowTitle('Message')
		self.msg.setWindowIcon(QIcon('server.ico'))

		self.progressbar = QProgressBar(self)
		self.progressbar.resize(350, 30)
		self.progressbar.move((self.width-self.progressbar.frameGeometry().width()+40)/2, 120)
		self.progressbar.hide()
		self.progresssig = progresssignal()
		self.progresssig.sig.connect(self.setprogressvalue)

		self.t1 = Thread(target = self.textuntilconnection)
		self.t1.setDaemon(True)
		self.t1.start()
		self.t2 = Thread(target = self.startserver)
		self.t2.setDaemon(True)
		self.t2.start()
		self.t3 = Thread(target = self.afterconnecting)
		self.t3.setDaemon(True)
		self.t3.start()
		self.t4 = Thread(target = self.afterfile)
		self.t4.setDaemon(True)
		self.t4.start()
		self.t5 = Thread(target = self.textduringtransfer)
		self.t5.setDaemon(True)
		self.t5.start()

		self.t = Queue()
		self.t.put(self.t1)
		self.t.put(self.t2)
		self.t.put(self.t3)
		self.t.put(self.t4)
		self.t.put(self.t5)

		self.show()
		self.isshown = True

	def center(self):
		cp = QDesktopWidget().availableGeometry().center()
		self.frame.moveCenter(cp)
		self.move(self.frame.topLeft())

	def textuntilconnection(self):
		global clientconnected

		while not clientconnected:
			if self.isshown:
				self.lbl2.setText('waiting for connections.')
				if not clientconnected:
					time.sleep(0.125)
				self.lbl2.setText('waiting for connections..')
				if not clientconnected:
					time.sleep(0.125)
				self.lbl2.setText('waiting for connections...')
				if not clientconnected:
					time.sleep(0.125)

	def removetext(self):
		time.sleep(0.125)
		self.lbl1.deleteLater()
		self.lbl2.deleteLater()

	def startserver(self):
		global clientconnected

		self.server = socket.socket() #create a socket object
		host = socket.gethostname()
		port = 9999 #port for the socket
		self.server.bind((host, port))
		self.server.listen(5)
		self.client, self.addr = self.server.accept()
		clientconnected = True

	def afterconnecting(self):
		wait()
		self.removetext()
		self.showdropbox()

	def afterfile(self):
		global filename

		while not filename:
			pass

		if os.path.isfile(filename):
			self.sendfile()
		else:
			self.senddirectory()

	def showdropbox(self):
		self.lbl3.show()

	def sendfile(self):
		global filename

		self.lbl3.deleteLater()
		self.progressbar.show()
		self.lbl4.show()

		f = open(filename, 'rb')
		l = f.read(4096)

		filesize = ((os.stat(filename)).st_size)
		filename = filename.split('/')
		filename = filename[len(filename)-1]
		lv1size = str(size_(filename))
		lv2size = str(size_(lv1size))

		self.client.send(lv2size.encode('ascii'))
		self.client.send(lv1size.encode('ascii'))

		print(lv1size)
		print(lv2size)
		print(filename)
		self.client.send(filename.encode('ascii'))

		datasentpercent = 0
		percentvalue = 409600/filesize
		while l:
			self.client.send(l)
			datasentpercent += percentvalue
			self.progresssig.sig.emit(int(datasentpercent))
			l = f.read(4096)

		f.close()

		self.client.close()
		self.transfer = True

		self.textaftertransfer()

	def senddirectory(self):
		global filename

		self.lblsig.sig.emit()
		filename = ''
		self.afterfile()

	def showfoldermsgbox(self):
		self.msg.exec_()

	def closeEvent(self, e):
		self.isshown = False
		e.accept()

	def centerwidget(self, a, pos):
		a.resize(a.sizeHint())
		a.move((self.width-a.frameGeometry().width())/2, pos)

	def textduringtransfer(self):
		global filename

		while not filename:
			if self.isshown:
				self.lbl4.setText('sending the file.')
				if not clientconnected:
					time.sleep(0.125)
				self.lbl4.setText('sending the file..')
				if not clientconnected:
					time.sleep(0.125)
				self.lbl4.setText('sending the file...')
				if not clientconnected:
					time.sleep(0.125)

	def textaftertransfer(self):
		self.progressbar.deleteLater()
		self.lbl4.deleteLater()
		self.lbl5.show()

	def setprogressvalue(self, v):
		self.progressbar.setValue(v)


if __name__ == '__main__':
	app = QApplication([])
	server = serverWindow()
	sys.exit(app.exec_())
