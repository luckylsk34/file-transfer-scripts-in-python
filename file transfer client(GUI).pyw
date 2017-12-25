import socket
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
from threading import Thread
from queue import Queue
import time
import shutil
import os

serverconnected = False

class Signal(QObject):
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
        self.lbl2 = QLabel('trying to connect...', self)
        self.centerwidget(self.lbl2, 130)
        self.lbl2.hide()
        self.lbl3 = QLabel('connected to server', self)
        self.centerwidget(self.lbl3, 130)
        self.lbl3.hide()
        self.lbl4 = QLabel('waiting for file or folder...', self)
        self.centerwidget(self.lbl4, 150)
        self.lbl4.hide()
        self.lbl5 = QLabel('recieving the file...', self)
        self.centerwidget(self.lbl5, 150)
        self.lbl5.hide()
        self.lbl6 = QLabel('transfer complete', self)
        self.centerwidget(self.lbl6, 120)
        self.lbl6.hide()
        self.host = ''
        self.hostinput = QLineEdit(self)
        self.hostinput.setText('192.168.1.107')
        self.hostinput.resize(100, 30)
        self.hostinput.move(150, 60)
        self.port = 9999

        self.connectbtn = QPushButton('connnect', self)
        self.centerwidget(self.connectbtn, 150)
        self.connectbtn.clicked.connect(self.sethostname)

        self.nohostmsg = QMessageBox()
        self.nohostmsg.setIcon(QMessageBox.Warning)
        self.nohostmsg.setText('Please enter a host')
        self.nohostmsg.setWindowTitle('Message')
        self.nohostmsg.setWindowIcon(QIcon('client.ico'))
        self.nohostsig = Signal()
        self.nohostsig.sig.connect(self.shownohostmsg)

        self.filedialogue = QFileDialog()
        self.filedialogue.setWindowIcon(QIcon('client.ico'))
        self.showdialoguesig = Signal()
        self.showdialoguesig.sig.connect(self.showfiledialogue)

        self.searchingforconnection = False
        self.filename = ''
        self.transfer = False
        self.copytofolder = ''

        self.t1 = Thread(target = self.textafterhostname)
        self.t1.setDaemon(True)
        self.t1.start()
        self.t2 = Thread(target = self.connecttoserver)
        self.t2.setDaemon(True)
        self.t2.start()
        self.t3 = Thread(target = self.textafterconnection)
        self.t3.setDaemon(True)
        self.t3.start()
        self.t4 = Thread(target = self.afterconnection)
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

    def center(self):
        cp = QDesktopWidget().availableGeometry().center()
        self.frame.moveCenter(cp)
        self.move(self.frame.topLeft())

    def centerwidget(self, a, pos):
        a.resize(a.sizeHint())
        a.move((self.width-a.frameGeometry().width())/2, pos)

    def sethostname(self):
        if self.hostinput.text():
            self.host = self.hostinput.text()
        else:
            self.nohostsig.sig.emit()

    def connecttoserver(self):
        global serverconnected

        while not self.host:
            pass

        self.client = socket.socket()
        while True:
            try:
                self.client.connect((self.host, self.port))
                serverconnected = True
                break
            except:
                pass

    def shownohostmsg(self):
        self.nohostmsg.exec_()

    def textafterhostname(self):
        while not self.host:
            pass

        self.lbl1.deleteLater()
        self.hostinput.deleteLater()
        self.connectbtn.deleteLater()
        self.lbl2.show()

        global serverconnected

        while not serverconnected:
            self.lbl2.setText('trying to connect.')
            if not serverconnected:
                time.sleep(0.125)
            self.lbl2.setText('trying to connect..')
            if not serverconnected:
                time.sleep(0.125)
            self.lbl2.setText('trying to connect...')
            if not serverconnected:
                time.sleep(0.125)

    def textafterconnection(self):
        global serverconnected

        while not serverconnected:
            pass
        time.sleep(0.125)

        self.lbl2.deleteLater()
        self.lbl3.show()
        self.lbl4.show()

        while not self.filename:
            self.lbl4.setText('waiting for file or folder.')
            if not self.filename:
                time.sleep(0.125)
            self.lbl4.setText('waiting for file or folder..')
            if not self.filename:
                time.sleep(0.125)
            self.lbl4.setText('waiting for file or folder...')
            if not self.filename:
                time.sleep(0.125)

    def afterconnection(self):
        global serverconnected

        while not serverconnected:
            pass

        if (self.client.recv(1)).decode('ascii') == '1':
            self.transfer = True
            self.recvfile()
        else:
            self.transfer = True
            self.recvfolder()

    def recvfile(self):

        self.lbl5.show()

        self.lv2size = (self.client.recv(1)).decode('ascii')
        self.lv1size = (self.client.recv(int(self.lv2size))).decode('ascii')
        self.filename = (self.client.recv(int(self.lv1size))).decode('ascii')

        c1 = time.time()
        tmpf = open('temporaryfile.tmp', 'wb')
        while True:
            data = self.client.recv(4096)
            if not data:
                break
            tmpf.write(data)
        tmpf.close()
        c2 = time.time()
        size = ((os.stat(self.filename)).st_size)/1024**2

        print('\nStats\nTime taken :%0.2f' % (c2-c1))
        print('size :%0.2f' % size, 'MB')
        print('Speed :%0.3f' % (size/(c2-c1)), 'MBps')

        self.showdialoguesig.sig.emit()
        while not self.copytofolder:
            pass
        shutil.copyfile('temporaryfile.tmp', self.copytofolder+'\\'+self.filename)
        os.remove('temporaryfile.tmp')

        self.transfer = False
        self.textaftertransfer()

    def textaftertransfer(self):
        time.sleep(0.125)
        self.lbl5.deleteLater()
        self.lbl6.show()

    def textduringtransfer(self):
        while not self.transfer:
            pass

        time.sleep(0.125)
        self.lbl3.deleteLater()
        self.lbl4.deleteLater()

        while self.transfer:
            self.lbl5.setText('recieving the file.')
            if self.transfer:
                time.sleep(0.125)
            self.lbl5.setText('recieving the file..')
            if self.transfer:
                time.sleep(0.125)
            self.lbl5.setText('recieving the file...')
            if self.transfer:
                time.sleep(0.125)

    def showfiledialogue(self):
        self.copytofolder = self.filedialogue.getExistingDirectory(self, "Select Directory")

if __name__ == '__main__':
    app = QApplication([])
    client = clientWindow()
    sys.exit(app.exec_())
