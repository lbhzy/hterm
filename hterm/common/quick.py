from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

import os
import sys
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
    def __init__(self):
        super().__init__()

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


if __name__ == "__main__":

    app = QApplication()

    w = QuickDialog()
    w.show()

    app.exec() 