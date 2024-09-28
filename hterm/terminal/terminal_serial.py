from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

import time
import serial

from terminal_base import Terminal


class SerialTerm(Terminal):
    """ 串口终端 """
    def __init__(self, port, baud):
        super().__init__()

        self.port = port
        self.baud = baud
        self.connected = False

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.timerCallback)

        self.open()
        
    def open(self):
        try:
            self.ser = serial.Serial(self.port, self.baud, timeout=0.01)
            self.timer.start(0)
            self.connected = True
            self.display(f"连接成功\n")
        except Exception as e:
            self.connected = False
            self.display(f"连接失败: {e}\n")

    def close(self):
        if self.connected:
            self.ser.close()
              
    def sendData(self, data):
        if self.connected:
            self.ser.write(data.encode("utf-8"))
        else:
            self.open()


    def timerCallback(self):
        try:
            data = None
            if self.ser.in_waiting:
                data = self.ser.readline()
        except Exception:
            self.connected = False
            self.display(f"连接断开\n")
            return
        
        if data:
            text = data.decode("utf-8", "replace")
            self.display(text)
            self.timer.start(0)
        else:
            self.timer.start(10)

if __name__ == "__main__":

    app = QApplication()
    
    term = SerialTerm("COM3", 115200)
    term.show()

    app.exec()