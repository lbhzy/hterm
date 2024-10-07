from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

import os
import sys
from PySide6.QtWidgets import QWidget
import serial.tools.list_ports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import Config
from ui.session_ui import Ui_SessionDialog

class SessionDialog(QDialog, Ui_SessionDialog):
    """ 会话创建 """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)

        self.tabWidget.setCurrentIndex(0)
        # SSH相关
        # self.ssh_name.setPlaceholderText('缺省使用服务器名称')
        self.ssh_port.setText('22')
        self.ssh_password.setEchoMode(QLineEdit.Password)
        # 串口相关
        # self.serial_name.setPlaceholderText('缺省使用串口名称')
        self.serial_baud.setEditable(True)
        self.serial_baud.addItems(['9600', '115200'])
        self.serial_baud.setCurrentIndex(1)
        self.serial_port.setEditable(True)
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.serial_port.addItem(port.device)
            print(f"设备: {port.device}, 描述: {port.description}, 硬件ID: {port.hwid}")


    def accept(self):
        index = self.tabWidget.currentIndex()
        if index == 0:
            session = {'name': self.ssh_name.text(), 
                        'type': 'ssh', 
                        'target': self.ssh_server.text(),
                        'port': int(self.ssh_port.text()),
                        'username': self.ssh_username.text(),
                        'password': self.ssh_password.text()
                        }
        elif index == 1:
            session = {'name': self.serial_name.text(), 
                        'type': 'serial', 
                        'target': self.serial_port.currentText(),
                        'baudrate': int(self.serial_baud.currentText())
                        }
        elif index == 2:
            session = {'name': self.shell_name.text(), 
                        'type': 'local', 
                        'target': self.shell_program.text()
                        }
        print(session)
        cfg = Config('session')
        cfg.addConfig(session)

        super().accept()

class SessionList(QListWidget):

    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)

        font = QFont()
        font.setPointSize(10)
        self.setFont(font)

        self.menu = QMenu(self)
        action = self.menu.addAction("新建会话")
        action.triggered.connect(lambda: SessionDialog(self).exec())

        self.item_menu = QMenu(self)
        action1 = self.item_menu.addAction("修改")
        action2 = self.item_menu.addAction("删除")


        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.menuHandler)

        cfg = Config('session')
        sessions = cfg.loadConfig()
        for session in sessions:
            self.addItem(session['name'])
        

    def menuHandler(self, pos):
        item = self.itemAt(pos)
        if item:
            menu = self.item_menu
        else:
            menu = self.menu
        
        menu.exec(self.mapToGlobal(pos))

if __name__ == "__main__":

    app = QApplication()

    w = SessionDialog()
    w.show()

    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.addWidget(SessionList(widget))
    widget.show()

    app.exec() 