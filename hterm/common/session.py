from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

import os
import sys
import qtawesome as qta
import serial.tools.list_ports
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from config import Config
from ui.session_ui import Ui_SessionDialog

class SessionDialog(QDialog, Ui_SessionDialog):
    """ 会话创建 """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)

    def exec(self):
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
            # print(f"设备: {port.device}, 描述: {port.description}, 硬件ID: {port.hwid}")
        return super().exec()

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

        cfg = Config('session')
        cfg.addConfig(session)

        super().accept()

class SessionList(QListWidget):
    """ 会话列表 """
    update_signal = Signal()

    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)

        font = QFont()
        font.setPointSize(10)
        self.setFont(font)

        dialog = SessionDialog(self)
        dialog.accepted.connect(self.updateSessionList)

        self.menu = QMenu(self)
        action = self.menu.addAction("新建会话")
        action.setIcon(qta.icon('ri.chat-new-fill'))
        action.triggered.connect(lambda: dialog.exec())

        self.item_menu = QMenu(self)
        mod_action = self.item_menu.addAction("修改")
        mod_action.setIcon(qta.icon('ei.edit'))
        del_action = self.item_menu.addAction("删除")
        del_action.setIcon(qta.icon('mdi.delete-alert'))
        del_action.triggered.connect(self.deletSession)


        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showMenu)

        self.updateSessionList()

    def deletSession(self):
        cfg = Config('session')
        sessions = cfg.loadConfig()
        del sessions[self.currentRow()]
        cfg.saveNewConfig(sessions)
        self.updateSessionList()

    def updateSessionList(self):
        self.clear()
        cfg = Config('session')
        sessions = cfg.loadConfig()
        for session in sessions:
            name = session['name'] if session['name'] else session['target']
            item = QListWidgetItem(name)
            if session['type'] == 'serial':
                item.setIcon(qta.icon('mdi6.serial-port'))
            elif session['type'] == 'ssh':
                item.setIcon(qta.icon('mdi.ssh'))
            elif session['type'] == 'local': 
                item.setIcon(qta.icon('ri.mini-program-line'))
            self.addItem(item)
        self.update_signal.emit()
        

    def showMenu(self, pos):
        item = self.itemAt(pos)
        if item:
            menu = self.item_menu
        else:
            menu = self.menu
        
        menu.exec(self.mapToGlobal(pos))

if __name__ == "__main__":

    app = QApplication()

    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.addWidget(SessionList(widget))
    widget.show()

    app.exec() 