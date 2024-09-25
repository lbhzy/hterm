from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

import os
import sys
import importlib
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from ui.quick_ui import Ui_Dialog

MSG0 = """例如:
echo "Hello Hterm" """
MSG1 = """例如:
import you_need

#程序会调用main方法,获取return返回的字符串,进行发送                                       
def main():
    
    return "The text you want to send" """

class QuickDialog(QDialog, Ui_Dialog):
    """ 快捷命令 """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)
        self.textEdit.setPlaceholderText(MSG0)
        self.comboBox.currentIndexChanged.connect(self.indexChanged)

    def indexChanged(self, index):
        if index == 1:
            self.textEdit.setPlaceholderText(MSG1)
        else:
            self.textEdit.setPlaceholderText(MSG0)

    def accept(self):
        print("confirm")
        super().accept()

class QuickButton(QPushButton):
    """ 快捷命令按钮 """
    def __init__(self):
        super().__init__()
        self.clicked.connect(self.send)

    def send(self):
        mod = importlib.import_module(f"scripts.quick.{self.text()}")
        text = mod.main()
        print(text)

if __name__ == "__main__":

    app = QApplication()

    w = QuickDialog()
    w.show()

    app.exec() 