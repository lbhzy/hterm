from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

import time
from winpty import PtyProcess

from terminal_base import Terminal


class LocalTerm(Terminal):
    """ 本地程序终端 """
    def __init__(self, prog: str, bg_img=None, scheme=None):
        super().__init__(bg_img, scheme)

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.timerCallback)

        try:
            self.proc = PtyProcess.spawn(prog, backend=1)
            # self.proc.fileobj.settimeout(0)
            self.proc.fileobj.setblocking(False)
            self.timer.start(10)
        except Exception as e:
            self.display(f"Exception: {e}\n")

    def close(self):
        self.proc.close(force=True)
        super().close()

    def sendData(self, data):
        self.proc.write(data)
        # print(f"s: {data}")

    def timerCallback(self):
        data = ''
        
        try:
            data = self.proc.read()
        except Exception:
            pass
        if data:
            # print(f"rx: {data.encode()}")
            self.display(data)
            self.timer.start(0)
        else:
            self.timer.start(10)


if __name__ == "__main__":

    app = QApplication()

    term = LocalTerm("powershell")
    term.show()

    app.exec()