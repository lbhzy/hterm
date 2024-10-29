from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

import time
import paramiko

from terminal_base import Terminal


class SSHTerm(Terminal):
    """ SSH终端 """
    def __init__(self, server, port, username, password, bg_img=None, scheme="Horizon Dark"):
        super().__init__(bg_img, scheme)

        self.server = server
        self.port = port
        self.username = username
        self.password = password

        self.connected = False

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.timerCallback)

        self.ssh = paramiko.SSHClient()
        # 允许连接不在 know_hosts 文件中的主机
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        self.open()


    def open(self):
        try:
            self.ssh.connect(self.server, self.port, self.username, self.password, timeout=1)
            self.channel = self.ssh.invoke_shell()
            self.channel.resize_pty(width=80, height=24)
            self.transport = self.ssh.get_transport()
            self.transport.set_keepalive(10)
            self.timer.start(0)
            self.connected = True
            self.display(f"\n{self.server}:{self.port} 连接成功\n")
        except Exception as e:
            self.connected = False
            self.display(f"\n{self.server}:{self.port} 连接失败：{e}\n")

    def close(self):
        self.ssh.close()
        super().close()

    def sendData(self, data):
        if self.connected:
            self.channel.send(data.encode("utf-8"))
        else:
            self.open()

    def timerCallback(self):
        if not self.transport.is_alive():
            self.connected = False
            self.display(f"\n\n{self.server}:{self.port} 连接断开\n")
            return
        
        if self.channel.recv_ready():
            data = self.channel.recv(512)
            # print(data)
            text = data.decode("utf-8", "replace")

            self.display(text)

            self.timer.start(0)
        else:
            self.timer.start(10)


if __name__ == "__main__":

    app = QApplication()

    term = SSHTerm("10.10.10.1", 22, "root", "8822185")
    term.show()

    app.exec()