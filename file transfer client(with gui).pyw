import socket
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from threading import Thread
from queue import Queue
import time

serverconnected = False

class msgSignal(QObject):
    sig = pyqtSignal()

class clientWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        self.setFixedSize(400, 300)
        self.frame = self.frameGeometry()
        self.width = self.frame.width()
        self.height = self.height()

        self.setWindowTitle('client')
        self.setWindowIcon(QIcon('client.ico'))
        self.center()

        self.lbl1 = QLabel('Host', self)
        self.lbl1.resize(self.lbl1.sizeHint())
        self.lbl1.move(90, 60)
        self.host = ''
        self.hostinput = QLineEdit(self)
        self.hostinput.setText('192.168.1.107')
        self.hostinput.resize(100, 30)
        self.hostinput.move(150, 60)
        self.port = 9999

        self.nohostmsg = QMessageBox()
        self.nohostmsg.setIcon(QMessageBox.Warning)
        self.nohostmsg.setText('Please enter a host')
        self.nohostmsg.setWindowTitle('Message')
        self.nohostmsg.setWindowIcon(QIcon('client.ico'))

        self.nohostsig = msgSignal()
        self.nohostsig.sig.connect(self.shownohostmsg)

        self.connectbtn = QPushButton('send', self)
        self.centerwidget(self.connectbtn, 150)
        self.connectbtn.clicked.connect(self.connecttoserver)

        #self.lbl1 = QLabel('waiting for connection...', self)
        #self.centerwidget(self.lbl1, 130)

        self.isshown = False

        '''self.t1 = Thread(target = self.textbeforeconnection)
        self.t1.setDaemon(True)
        self.t1.start()
        self.t2 = Thread(target = self.connectoserver)
        self.t2.setDaemon(True)
        self.t2.start()'''

        self.t = Queue()

        #self.t.put(self.t1)
        #self.t.put(self.t2)

        self.show()
        self.isshown = True

    def center(self):
        cp = QDesktopWidget().availableGeometry().center()
        self.frame.moveCenter(cp)
        self.move(self.frame.topLeft())

    def centerwidget(self, a, pos):
        a.resize(a.sizeHint())
        a.move((self.width-a.frameGeometry().width())/2, pos)

    def textbeforeconnection(self):
        global serverconnected

        while not serverconnected:
            if self.isshown:
                self.lbl1.setText('waiting for connection.')
                if not serverconnected:
                    time.sleep(0.125)
                self.lbl1.setText('waiting for connection..')
                if not serverconnected:
                    time.sleep(0.125)
                self.lbl1.setText('waiting for connection...')
                if not serverconnected:
                    time.sleep(0.125)

    def connecttoserver(self):
        self.client = socket.socket()

        if self.hostinput.text():
            self.host = self.hostinput.text()

            while True:
                try:
                    self.client.connect((self.host, self.port))
                    break
                except:
                    time.sleep(0.125)
        else:
            self.nohostsig.sig.emit()

    def shownohostmsg(self):
        self.nohostmsg.exec_()

if __name__ == '__main__':
    app = QApplication([])
    client = clientWindow()
    sys.exit(app.exec_())
