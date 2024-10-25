from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

import os
import re
import sys
import importlib.util

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from ui.trigger_ui import Ui_Dialog
from terminal.terminal_base import Terminal
from config import Config


class Trigger(QObject):
    """ 触发器 """
    text_added = Signal(str)

    def __init__(self, term: Terminal) -> None:
        super().__init__()
        self.text_added.connect(self.handler)
        self.update()

    def update(self):
        self.triggers = Config("trigger").loadConfig()

    def handler(self, text):
        for trigger in self.triggers:
            matches = re.finditer(trigger['pattern'], text)
            for match in matches:
                print("match")
                if trigger['action'] == 'send text':
                    if trigger['type'] == 'text':
                        pass
                    elif trigger['type'] == 'script':
                        pass


class TriggerDialog(QDialog, Ui_Dialog):
    """ 触发器 """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("触发器管理")


if __name__ == '__main__':

    app = QApplication()

    w = TriggerDialog()
    w.show()

    app.exec() 