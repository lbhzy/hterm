from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

from terminal import Terminal
import time
import serial

class SerialTerm(Terminal):
    """ 串口终端 """
    def __init__(self, port, baud):
        super().__init__()

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.timerCallback)
        
        try:
            self.ser = serial.Serial(port, baud, timeout=0.01)
            self.timer.start(0)
        except Exception as e:
            self.display(f"Error: {e}")
              
    def sendData(self, data):
        if self.ser.is_open:
            self.ser.write(data.encode("utf-8"))


    def timerCallback(self):
        if self.ser.in_waiting > 0:
            data = self.ser.readline()
            text = data.decode('utf-8')
            self.display(text)
            self.timer.start(0)
        else:
            self.timer.start(10)

if __name__ == "__main__":

    app = QApplication()
    term = SerialTerm("COM3", 115200)
    term.show()
    app.exec()