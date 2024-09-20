from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from ui.quick_ui import Ui_Dialog

class QuickDialog(QDialog, Ui_Dialog):
    """ 快捷命令 """
    def __init__(self):
        super().__init__()

        self.setupUi(self)


    def accept(self):
        print("confirm")
        super().accept()


if __name__ == "__main__":

    app = QApplication()

    w = QuickDialog()
    w.show()

    app.exec() 