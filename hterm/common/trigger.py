from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

import os
import re
import sys
import importlib.util

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), "terminal"))

from ui.trigger_ui import Ui_Dialog
from terminal.terminal_base import Terminal
from config import Config


MSG0 = """例如:
echo "Hello Hterm"{^C}
{delay 10}
echo "10ms later"

特殊字段
{match}         匹配到的字符串
{^[A-Z]}        发送 CTRL+[A-Z]
{delay n}       延时 n 毫秒
"""
MSG1 = """例如:
import you_need

#程序会调用main方法,入参为匹配到的字符串,获取return返回的字符串,进行发送                                       
def main(match):
    
    return f"The matched text is {match}" """


def runPythonString(match, s):
    try:
        spec = importlib.util.spec_from_loader('script', loader=None)
        script = importlib.util.module_from_spec(spec)
        exec(s, script.__dict__)
        text = script.main(match)
    except Exception as e:
        return ''

    if not isinstance(text, str):
        return ''
    return text


class Trigger(QObject):
    """ 触发器 """
    text_added = Signal(str)
    text_send = Signal(str)

    def __init__(self, term: Terminal) -> None:
        super().__init__()
        self.text_added.connect(self.handler)
        self.update()

    def update(self):
        self.triggers = Config("trigger").loadConfig()

    def handler(self, text):
        for trigger in self.triggers:
            if not trigger['enable']:
                continue
            matches = re.finditer(trigger['pattern'], text)
            for match in matches:
                if trigger['action'] == 'send text':
                    if trigger['type'] == 'text':
                        res = trigger['content'].replace("{match}", match.group())
                    elif trigger['type'] == 'script':
                        res = runPythonString(match.group(), trigger['content'])
                    self.text_send.emit(res)


class TriggerDialog(QDialog, Ui_Dialog):
    """ 触发器 """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("触发器管理")
        self.setWindowFlag(Qt.WindowMaximizeButtonHint)

        self.plainTextEdit.setPlaceholderText(MSG0)
        self.listWidget.itemChanged.connect(self.itemChanged)
        self.listWidget.currentRowChanged.connect(self.currentRowChanged)
        self.name_edit.textChanged.connect(self.nameChanged)
        self.pattern_edit.textChanged.connect(self.patternChanged)
        self.type_combobox.currentIndexChanged.connect(self.typeChanged)
        self.plainTextEdit.textChanged.connect(self.contentChanged)
        self.add_button.clicked.connect(self.add)
        self.del_button.clicked.connect(self.delete)

        self.triggers = Config("trigger").loadConfig()
        for trigger in self.triggers:
            item = QListWidgetItem(trigger["name"])
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            if trigger['enable']:
                item.setCheckState(Qt.Checked)
            else:
                item.setCheckState(Qt.Unchecked)
            self.listWidget.addItem(item)
        self.listWidget.setCurrentRow(0)

    def nameChanged(self, text):
        row = self.listWidget.currentRow()
        if row < 0:
            return
        self.listWidget.currentItem().setText(text)
        self.triggers[row]["name"] = text

    def typeChanged(self, type_):
        row = self.listWidget.currentRow()
        if type_ == 1:
            self.plainTextEdit.setPlaceholderText(MSG1)
        else:
            self.plainTextEdit.setPlaceholderText(MSG0)
        if row < 0:
            return
        self.triggers[row]["type"] = 'script' if type_ else 'text'

    def patternChanged(self, text):
        row = self.listWidget.currentRow()
        if row < 0:
            return
        self.triggers[row]["pattern"] = text

    def contentChanged(self):
        row = self.listWidget.currentRow()
        if row < 0:
            return
        text = self.plainTextEdit.toPlainText()
        self.triggers[row]["content"] = text

    def currentRowChanged(self, row):
        if row < 0:
            self.name_edit.setText("")
            self.pattern_edit.setText("")
            self.plainTextEdit.setPlainText("")
            return
        # print(self.triggers[row])
        self.name_edit.setText(self.triggers[row]["name"])
        self.pattern_edit.setText(self.triggers[row]["pattern"])
        self.type_combobox.setCurrentIndex(0 if self.triggers[row]["type"] == "text" else 1)
        self.plainTextEdit.setPlainText(self.triggers[row]["content"])

    def itemChanged(self, item):
        row = self.listWidget.row(item)
        if item.checkState() == Qt.Checked:
            self.triggers[row]['enable'] = True
        elif item.checkState() == Qt.Unchecked:
            self.triggers[row]['enable'] = False

    def add(self):
        self.triggers.append({'name': '未命名',
                              'enable': True,
                              'pattern': '',
                              'action': 'send text',
                              'type': 'text',
                              'content': ''})
        item = QListWidgetItem("未命名")
        item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        item.setCheckState(Qt.Checked)
        self.listWidget.addItem(item)
        self.listWidget.setCurrentRow(self.listWidget.count() - 1)
        self.name_edit.selectAll()
        self.name_edit.setFocus()

    def delete(self):
        if self.listWidget.count() > 0:
            res = QMessageBox.warning(self, "删除触发器", "确定要删除选定项吗？",
                                QMessageBox.StandardButtons(QMessageBox.Yes | QMessageBox.No))
            if res == QMessageBox.No:
                return
            row = self.listWidget.currentRow()
            self.listWidget.takeItem(row)
            del self.triggers[row]

    def accept(self):
        Config("trigger").saveNewConfig(self.triggers)
        super().accept()


if __name__ == '__main__':

    app = QApplication()

    w = TriggerDialog()
    w.show()

    app.exec() 