from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

import os
import sys
import importlib.util
import qtawesome as qta

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from ui.quick_ui import Ui_Dialog
from config import Config

MSG0 = """例如:
echo "Hello Hterm" """
MSG1 = """例如:
import you_need

#程序会调用main方法,获取return返回的字符串,进行发送                                       
def main():
    
    return "The text you want to send" """

def runPythonString(parent, s):
    try:
        spec = importlib.util.spec_from_loader('script', loader=None)
        script = importlib.util.module_from_spec(spec)
        exec(s, script.__dict__)
        text = script.main()
    except Exception as e:
        QMessageBox.critical(parent, "执行脚本出错", str(e))
        return

    if not isinstance(text, str):
        QMessageBox.critical(parent, "执行脚本出错", f"返回类型{type(text)}，请返回str类型")
        return
    return text

class QuickDialog(QDialog, Ui_Dialog):
    """ 快捷命令 """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setupUi(self)
        self.setWindowTitle("快捷命令")
        self.textEdit.setPlaceholderText(MSG0)
        self.listWidget.currentRowChanged.connect(self.showQuick)
        self.comboBox.currentIndexChanged.connect(self.typeChanged)
        self.lineEdit.textChanged.connect(self.nameChanged)
        self.textEdit.textChanged.connect(self.contentChanged)
        self.addButton.clicked.connect(self.add)
        self.delButton.clicked.connect(self.delete)
        self.pushButton.clicked.connect(self.testRun)
        
        self.cfg = Config("quick")
        self.quicks = self.cfg.loadConfig()
        for quick in self.quicks:
            self.listWidget.addItem(quick["name"])
        self.listWidget.setCurrentRow(0)
        

    def contentChanged(self):
        index = self.listWidget.currentRow()
        if index < 0:
            return
        text = self.textEdit.toPlainText()
        self.quicks[index]["content"] = text

    def typeChanged(self, type):
        index = self.listWidget.currentRow()
        if index < 0:
            return
        if type == 1:
            self.textEdit.setPlaceholderText(MSG1)
            self.quicks[index]["type"] = "script"
        else:
            self.textEdit.setPlaceholderText(MSG0)
            self.quicks[index]["type"] = "text"

    def nameChanged(self, text):
        index = self.listWidget.currentRow()
        if index < 0:
            return
        self.listWidget.currentItem().setText(text)
        self.quicks[index]["name"] = text

    def testRun(self):
        text = self.textEdit.toPlainText()

        if self.comboBox.currentIndex() == 1:
            text = runPythonString(self, text)
        
        if text:
            QMessageBox.information(self, "运行成功", text)            

    def showQuick(self, index):
        if self.listWidget.currentRow() < 0:
            self.lineEdit.setText("")
            # self.comboBox.setEditText("")
            self.textEdit.setText("")
            return
        self.lineEdit.setText(self.quicks[index]["name"])
        self.comboBox.setCurrentIndex(0 if self.quicks[index]["type"] == "text" else 1)
        self.textEdit.setText(self.quicks[index]["content"])

    def add(self):
        index = self.listWidget.currentRow()
        self.listWidget.insertItem(index, "未命名")
        item = {'name': '未命名', 'type': 'text', 'content': ''}
        self.quicks.insert(index, item)
        if index == -1:
            self.listWidget.setCurrentRow(0)
        else:
            self.listWidget.setCurrentRow(index)


    def delete(self):
        if self.listWidget.count() > 0:
            index = self.listWidget.currentRow()
            self.listWidget.takeItem(index)
            del self.quicks[index]
        


    def accept(self):
        self.cfg.saveNewConfig(self.quicks)
        super().accept()

class QuickButton(QPushButton):
    """ 快捷命令按钮 """
    send_signal = Signal(str)

    def __init__(self, name, content_type, content):
        super().__init__()

        self.content_type = content_type
        self.content = content

        self.setText(name)
        self.setIcon(qta.icon('mdi6.arrow-up-bold-circle', color="green"))

        # 设置按钮尺寸 适应文本长度
        metrics = QFontMetrics(self.font())
        width = metrics.horizontalAdvance(name)
        self.setFixedSize(width + 20 + 10, 20)
        
        self.setFocusPolicy(Qt.NoFocus)

        self.clicked.connect(self.send)

    def send(self):
        if self.content_type == "text":
            text = self.content
        elif self.content_type == "script":
            text = runPythonString(self, self.content)
        
        if text:
            self.send_signal.emit(text)


class QuickBar(QWidget):
    """ 快捷命令栏 """
    send_signal = Signal(str)

    def __init__(self, parent = ..., f = None):
        if f:
            super().__init__(parent, f)
        else:
            super().__init__(parent)

        self.widget = QHBoxLayout(self)
        self.widget.setSpacing(0)
        self.widget.setContentsMargins(0, 0, 0, 0)

        self.layout = QHBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.button = QPushButton(qta.icon('mdi.speedometer'), "快捷命令")
        self.button.setFixedSize(80, 20)
        self.button.setFocusPolicy(Qt.NoFocus)
        self.button.setStyleSheet("""
            QPushButton {
                    border: none;
            }   
            QPushButton:hover {
                    background-color: #dddddd;
            }  
        """)
        self.button.clicked.connect(self.openDialog)

        self.widget.addWidget(self.button)
        self.widget.addLayout(self.layout)
        self.widget.addItem(QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))

        self.updateBar()

    def openDialog(self):
        dialog = QuickDialog(self)
        dialog.accepted.connect(self.updateBar)
        dialog.exec()

    def updateBar(self):
        while self.layout.count():
            item = self.layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        config = Config("quick")
        quicks = config.loadConfig()
        for quick in quicks:
            button = QuickButton(quick['name'], quick['type'], quick['content'])
            button.send_signal.connect(self.send_signal)
            self.layout.addWidget(button)


if __name__ == "__main__":

    app = QApplication()

    w = QuickBar(None, Qt.Window)
    w.send_signal.connect(lambda text: print(text))
    w.show()

    app.exec() 