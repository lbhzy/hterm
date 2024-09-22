from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from ui.session_ui import Ui_SessionDialog

class SessionDialog(QDialog, Ui_SessionDialog):
    """ 会话创建 """
    def __init__(self):
        super().__init__()

        self.setupUi(self)


    def accept(self):
        print("confirm")
        super().accept()


if __name__ == "__main__":

    app = QApplication()

    w = SessionDialog()
    w.show()

    app.exec() 