from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

import os
import sys
import importlib.util

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from ui.tigger_ui import Ui_Dialog
from config import Config


class Tigger:
    """ 触发器 """
    def __init__(self) -> None:
        pass


class TiggerDialog(QDialog, Ui_Dialog):
    """ 触发器 """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("触发器管理")


if __name__ == '__main__':

    app = QApplication()

    w = TiggerDialog()
    w.show()

    app.exec() 