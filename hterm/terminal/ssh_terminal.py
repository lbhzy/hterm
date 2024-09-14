from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

import time
import paramiko
from terminal import Terminal


class SSHTerm(Terminal):
    """ SSH终端 """
    def __init__(self, server, port, username, password):
        super().__init__()

        self.server = server
        self.port = port
        self.username = username
        self.password = password

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.timerCallback)

        self.ssh = paramiko.SSHClient()
        # 允许连接不在 know_hosts 文件中的主机
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        self.connect()


    def connect(self):
        try:
            self.ssh.connect(self.server, self.port, self.username, self.password, timeout=1)
            self.display("SSH connect successful\n")
            self.channel = self.ssh.invoke_shell(term="hterm", width=80)
            self.channel.resize_pty(width=80, height=24)
            self.transport = self.ssh.get_transport()
            self.transport.set_keepalive(10)
            self.timer.start(0)
        except Exception as e:
            self.display(f"Exception: {e}\n")

    def sendData(self, data):
        if self.ssh.get_transport().is_active():
            self.channel.send(data.encode("utf-8"))

    def timerCallback(self):
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