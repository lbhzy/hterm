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
        text = self.textEdit.toPlainText()
        self.quicks[index]["content"] = text

    def typeChanged(self, type):
        index = self.listWidget.currentRow()
        if type == 1:
            self.textEdit.setPlaceholderText(MSG1)
            self.quicks[index]["type"] = "script"
        else:
            self.textEdit.setPlaceholderText(MSG0)
            self.quicks[index]["type"] = "text"

    def nameChanged(self, text):
        index = self.listWidget.currentRow()
        self.listWidget.currentItem().setText(text)
        self.quicks[index]["name"] = text

    def testRun(self):
        text = self.textEdit.toPlainText()
        if self.comboBox.currentIndex() == 1:
            try:
                spec = importlib.util.spec_from_loader('script', loader=None)
                script = importlib.util.module_from_spec(spec)
                exec(text, script.__dict__)
                text = script.main()
            except Exception as e:
                QMessageBox.critical(self, "执行脚本出错", str(e))
                return
        
        if isinstance(text, str):
            if text:
                QMessageBox.information(self, "运行成功", text)  
        else:
            QMessageBox.critical(self, "执行脚本出错", f"返回类型{type(text)}，请返回str类型")            

    def showQuick(self, index):
        if self.listWidget.currentRow() >= 0:
            self.lineEdit.setEnabled(True)
            self.comboBox.setEnabled(True)
            self.textEdit.setEnabled(True)
        else:
            self.lineEdit.setText("")
            self.comboBox.setEditText("")
            self.textEdit.setText("")
            self.textEdit.setPlaceholderText("")
            self.lineEdit.setDisabled(True)
            self.comboBox.setDisabled(True)
            self.textEdit.setEnabled(False)
            return
        self.lineEdit.setText(self.quicks[index]["name"])
        self.comboBox.setCurrentIndex(0 if self.quicks[index]["type"] == "text" else 1)
        self.textEdit.setText(self.quicks[index]["content"])

    def add(self):
        index = self.listWidget.currentRow() + 1
        self.listWidget.insertItem(index, "未命名")
        item = {'name': '未命名', 'type': 'text', 'content': ''}
        self.quicks.insert(index, item)
        self.listWidget.setCurrentRow(index)


    def delete(self):
        if self.listWidget.count() > 0:
            index = self.listWidget.currentRow()
            self.listWidget.takeItem(index)
            del self.quicks[index]
            print(self.listWidget.currentRow())
        


    def accept(self):
        self.cfg.saveNewConfig(self.quicks)

        layout = self.parent().findChild(QHBoxLayout)
        while True:
            item = layout.itemAt(1)
            if isinstance(item.widget(), QPushButton):
                widget = item.widget()
                layout.removeWidget(widget)
                widget.deleteLater()
            else:
                break
        for quick in reversed(self.quicks):
            button = QuickButton(quick['type'], quick['content'])
            button.setText(quick['name'])
            button.setIcon(qta.icon('fa.send-o'))
            layout.insertWidget(1, button)
        # for child in self.parent().children():
        #     if isinstance(child, QPushButton):
        #         main_widget.removeChild(child)
        #         child.deleteLater()
        super().accept()

class QuickButton(QPushButton):
    """ 快捷命令按钮 """
    def __init__(self, content_type, content):
        super().__init__()

        self.content_type = content_type
        self.content = content

        self.setFocusPolicy(Qt.NoFocus)
        self.clicked.connect(self.send)

    def send(self):
        if self.content_type == "text":
            text = self.content
        elif self.content_type == "script":
            try:
                spec = importlib.util.spec_from_loader('script', loader=None)
                script = importlib.util.module_from_spec(spec)
                exec(self.content, script.__dict__)
                text = script.main()
            except Exception as e:
                QMessageBox.critical(self, "执行脚本出错", str(e))
                return
        
        if isinstance(text, str):
            if text:
                tabWidget :QTabWidget = self.parent().findChildren(QTabWidget)[0]
                # 找到当前在前台的终端
                term = tabWidget.currentWidget()
                if term:
                    term.preSendData(text)
        else:
            QMessageBox.critical(self, "执行脚本出错", f"返回类型{type(text)}，请返回str类型")


if __name__ == "__main__":

    app = QApplication()

    w = QuickDialog()
    w.show()

    app.exec() 