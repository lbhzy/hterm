from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

import os
import sys
import importlib.util

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
    def __init__(self, type, content):
        super().__init__()

        self.type = type
        self.content = content

        self.setFocusPolicy(Qt.NoFocus)
        self.clicked.connect(self.send)

    def send(self):
        if self.type == "text":
            text = self.content
        elif self.type == "script":
            try:
                spec = importlib.util.spec_from_loader('script', loader=None)
                script = importlib.util.module_from_spec(spec)
                exec(self.content, script.__dict__)
                text = script.main()
            except Exception as e:
                QMessageBox.critical(self, "执行脚本出错", str(e))
                return
        
        print(text)


if __name__ == "__main__":

    app = QApplication()

    w = QuickDialog()
    w.show()

    app.exec() 