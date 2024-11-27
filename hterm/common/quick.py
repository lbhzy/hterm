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
echo "Hello Hterm"{^C}
{delay 10}
echo "10ms later"

特殊字段
{^[A-Z]}        发送 CTRL+[A-Z]
{delay n}       延时 n 毫秒
"""
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
        self.setWindowFlag(Qt.WindowMaximizeButtonHint)
        self.plainTextEdit.setPlaceholderText(MSG0)

        self.addButton.setIcon(qta.icon('mdi.plus'))
        self.delButton.setIcon(qta.icon('mdi.minus'))
        self.upButton.setIcon(qta.icon('fa.angle-up'))
        self.downButton.setIcon(qta.icon('fa.angle-down'))

        self.listWidget.currentRowChanged.connect(self.itemChanged)
        self.comboBox.currentIndexChanged.connect(self.typeChanged)
        self.lineEdit.textChanged.connect(self.nameChanged)
        self.plainTextEdit.textChanged.connect(self.contentChanged)
        self.addButton.clicked.connect(self.add)
        self.delButton.clicked.connect(self.delete)
        self.upButton.clicked.connect(self.up)
        self.downButton.clicked.connect(self.down)
        self.pushButton.clicked.connect(self.testRun)
        
        self.quicks = Config("quick").loadConfig()
        for quick in self.quicks:
            self.listWidget.addItem(quick["name"])
        self.listWidget.setCurrentRow(0)
        
    def contentChanged(self):
        index = self.listWidget.currentRow()
        if index < 0:
            return
        text = self.plainTextEdit.toPlainText()
        self.quicks[index]["content"] = text

    def typeChanged(self, type_):
        index = self.listWidget.currentRow()
        if type_ == 1:
            self.plainTextEdit.setPlaceholderText(MSG1)
        else:
            self.plainTextEdit.setPlaceholderText(MSG0)
        if index < 0:
            return
        self.quicks[index]["type"] = 'script' if type_ else 'text'

    def nameChanged(self, text):
        index = self.listWidget.currentRow()
        if index < 0:
            return
        self.listWidget.currentItem().setText(text)
        self.quicks[index]["name"] = text          

    def itemChanged(self, index):
        if self.listWidget.currentRow() < 0:
            self.lineEdit.setText("")
            self.plainTextEdit.setPlainText("")
            return
        self.lineEdit.setText(self.quicks[index]["name"])
        self.comboBox.setCurrentIndex(0 if self.quicks[index]["type"] == "text" else 1)
        self.plainTextEdit.setPlainText(self.quicks[index]["content"])
    
    def testRun(self):
        text = self.plainTextEdit.toPlainText()
        if self.comboBox.currentIndex() == 1:
            text = runPythonString(self, text)
        if text:
            QMessageBox.information(self, "运行成功", text)

    def add(self):
        self.quicks.append({'name': '未命名', 'type': 'text', 'content': ''})
        self.listWidget.addItem("未命名")
        self.listWidget.setCurrentRow(self.listWidget.count() - 1)
        self.lineEdit.selectAll()
        self.lineEdit.setFocus()

    def delete(self):
        if self.listWidget.count() > 0:
            res = QMessageBox.warning(self, "删除命令", "确定要删除选定命令吗？",
                                QMessageBox.StandardButtons(QMessageBox.Yes | QMessageBox.No))
            if res == QMessageBox.No:
                return
            index = self.listWidget.currentRow()
            self.listWidget.takeItem(index)
            del self.quicks[index]

    def up(self):
        row = self.listWidget.currentRow()
        if row > 0:
            self.quicks[row], self.quicks[row - 1] = self.quicks[row - 1], self.quicks[row]
            item = self.listWidget.currentItem()
            text = item.text()
            self.listWidget.setCurrentRow(row - 1)
            item.setText(self.listWidget.currentItem().text())
            self.listWidget.currentItem().setText(text)

    def down(self):
        row = self.listWidget.currentRow()
        if row < self.listWidget.count() - 1:
            self.quicks[row], self.quicks[row + 1] = self.quicks[row + 1], self.quicks[row]
            item = self.listWidget.currentItem()
            text = item.text()
            self.listWidget.setCurrentRow(row + 1)
            item.setText(self.listWidget.currentItem().text())
            self.listWidget.currentItem().setText(text)       
        
    def accept(self):
        Config("quick").saveNewConfig(self.quicks)
        super().accept()

class QuickButton(QPushButton):
    """ 快捷命令按钮 """
    send_signal = Signal(str)

    def __init__(self, name, type_, content):
        super().__init__()

        self.type = type_
        self.content = content

        self.setText(name)
        if type_ == "text":
            self.setIcon(qta.icon('ph.text-t-bold', color="green"))
        elif type_ == "script":
            self.setIcon(qta.icon('ph.code-bold', color="blue"))
        # 设置按钮尺寸 适应文本长度
        metrics = QFontMetrics(self.font())
        width = metrics.horizontalAdvance(name)
        self.setFixedSize(width + 20 + 10, 20)

        self.setFocusPolicy(Qt.NoFocus)

        self.clicked.connect(self.send)

    def send(self):
        if self.type == "text":
            text = self.content
        elif self.type == "script":
            text = runPythonString(self, self.content)
        
        if text:
            self.send_signal.emit(text)


class QuickBar(QWidget):
    """ 快捷命令栏 """
    send_signal = Signal(str)

    def __init__(self, parent=None, f=None):
        if f:
            super().__init__(parent, f)
        else:
            super().__init__(parent)

        self.widget = QHBoxLayout(self)
        self.widget.setSpacing(0)
        self.widget.setContentsMargins(0, 0, 0, 0)

        self.layout = QHBoxLayout()
        self.layout.setSpacing(1)
        self.layout.setContentsMargins(0, 1, 0, 1)

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

    w = QuickBar(f=Qt.Window)
    w.send_signal.connect(lambda text: print(text))
    w.show()

    app.exec() 