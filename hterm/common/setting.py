from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

import os
import sys
import qtawesome as qta

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'terminal'))

from terminal.terminal_base import Terminal
from ui.setting_ui import Ui_Dialog
from config import Config
from terminal.color import Color


class SettingDialog(QDialog, Ui_Dialog):
    """ 快捷命令 """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowMaximizeButtonHint)

        self.term = None
        self.setting = Config("setting").loadConfig()
        self.spinBox.setValue(self.setting['terminal']['size'])
        self.fontComboBox.setWritingSystem(QFontDatabase.WritingSystem.Latin)
        self.fontComboBox.setFontFilters(QFontComboBox.FontFilter.MonospacedFonts)
        self.fontComboBox.setCurrentFont(self.setting['terminal']['fonts'][0])
        self.fontComboBox_2.setWritingSystem(QFontDatabase.WritingSystem.SimplifiedChinese)
        self.fontComboBox_2.setCurrentFont(self.setting['terminal']['fonts'][1])
        schemes = Color().getSchemes()
        self.listWidget.addItems(schemes)
        self.listWidget.setCurrentRow(schemes.index(self.setting['terminal']['scheme']))
        self.listWidget.setFixedHeight(150)
        self.checkBox.setChecked(self.setting['terminal']['background'])
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.argv[0])
        else:
            base_dir = os.path.dirname(os.path.dirname(__file__))
        self.images_dir = os.path.join(base_dir, "images")
        images = []
        names = os.listdir(self.images_dir)
        for name in names:
            images.append(name)
        self.comboBox.addItems(images)

        self.spinBox.valueChanged.connect(self.createTerm)
        self.fontComboBox.currentFontChanged.connect(self.createTerm)
        self.fontComboBox_2.currentFontChanged.connect(self.createTerm)
        self.checkBox.stateChanged.connect(self.createTerm)
        self.comboBox.currentIndexChanged.connect(self.createTerm)
        self.listWidget.currentRowChanged.connect(self.createTerm)
        self.createTerm()

    def createTerm(self):
        if self.term:
            self.term.deleteLater()
        image = None
        if self.checkBox.isChecked():
            if self.comboBox.currentText():
                image = os.path.join(self.images_dir, self.comboBox.currentText())
        self.term = Terminal(image, self.listWidget.currentItem().text())
        self.gridLayout.addWidget(self.term, 0, 1)
        font = QFont()
        font.setPointSize(self.spinBox.value())
        font.setFamily(self.fontComboBox_2.currentText())
        char_format = QTextCharFormat()
        char_format.setFont(font)
        self.term.setCurrentCharFormat(char_format)
        self.term.append("终端外观")
        font.setFamily(self.fontComboBox.currentText())
        char_format.setFont(font)
        self.term.setCurrentCharFormat(char_format)
        self.term.append("abc123456")


if __name__ == '__main__':

    app = QApplication()

    w = SettingDialog()
    w.show()

    app.exec() 