from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

import os
import sys
import time
if sys.platform == 'win32':
    from winpty import PtyProcess
else:
    import pty

from terminal_base import Terminal


class LocalTerm(Terminal):
    """ 本地程序终端 """
    def __init__(self, prog: str, bg_img=None, scheme=None):
        super().__init__(bg_img, scheme)

        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.timerCallback)

        try:
            if sys.platform == 'win32':
                # Windows 使用 winpty
                self.proc = PtyProcess.spawn(prog, backend=1)
                self.proc.fileobj.setblocking(False)
            else:
                # Unix 使用 pty.fork
                pid, fd = pty.fork()
                if pid == 0:
                    # 子进程执行目标程序
                    os.execvp(prog, [prog])
                else:
                    # 父进程保存 fd
                    self.proc_pid = pid
                    self.proc_fd = fd

            self.timer.start(10)
        except Exception as e:
            self.display(f"Exception: {e}\n")

    def close(self):
        if sys.platform == 'win32':
            self.proc.close(force=True)
        else:
            try:
                os.close(self.proc_fd)
            except Exception:
                pass
        super().close()

    def sendData(self, data: str):
        if sys.platform == 'win32':
            self.proc.write(data)
        else:
            os.write(self.proc_fd, data.encode())

    def timerCallback(self):
        data = ''
        try:
            if sys.platform == 'win32':
                data = self.proc.read()
            else:
                # 非阻塞读取伪终端输出
                import select
                r, _, _ = select.select([self.proc_fd], [], [], 0)
                if r:
                    data = os.read(self.proc_fd, 1024).decode(errors="ignore")
        except Exception:
            pass

        if data:
            self.display(data)
            self.timer.start(0)
        else:
            self.timer.start(10)


if __name__ == "__main__":
    app = QApplication()

    # Windows 下用 powershell，Linux/macOS 下用 bash
    prog = "powershell" if sys.platform == "win32" else "bash"
    term = LocalTerm(prog)
    term.show()

    app.exec()
