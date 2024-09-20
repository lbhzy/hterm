from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

import os
import sys
import qtawesome as qta

sys.path.append(os.path.join(os.path.dirname(__file__), 'terminal'))

from ui.form_ui import Ui_MainWindow
from common.quick import QuickDialog
from common.config import Config
from terminal.terminal_ssh import SSHTerm
from terminal.terminal_local import LocalTerm
from terminal.terminal_serial import SerialTerm



class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(qta.icon('ph.terminal-window-fill'))
        # self.setWindowIcon(qta.icon('ph.terminal-window-light'))
        self.resize(QGuiApplication.primaryScreen().size()*0.6)

        self.ui.newSession.triggered.connect(lambda: QuickDialog().exec())
        
        self.setWindowTitle("hterm")
        self.ui.tabWidget.setTabsClosable(True)
        self.ui.tabWidget.setStyleSheet("QTabBar::tab { height: 25px; }")
        self.setWindowOpacity(0.95)

        left_widget = QLabel("🟢就绪")
        self.ui.statusbar.addWidget(left_widget, 1)  # 左侧信息，权重为 1

        right_widget = QLabel("2024-8-16 0:11")
        self.ui.statusbar.addWidget(right_widget, 0)  # 右侧信息，权重为 0

        config = Config()
        session_list = config.loadConfig()
        for item in session_list:
            self.ui.listWidget.addItem(item['name'])
            # print(item)
        cfg = config.getConfigByName("openwrt")
        self.openSession(cfg)
        cfg = config.getConfigByName("powershell")
        self.openSession(cfg)

    def openSession(self, cfg):
        if cfg['type'] == 'ssh':
            term = SSHTerm(cfg['target'], cfg['port'], cfg['username'], cfg['password'])
        elif cfg['type'] == 'serial':
            term = SerialTerm(cfg['target'], cfg['baud'])
        elif cfg['type'] == 'local':
            term = LocalTerm(cfg['target'])

        tab = QWidget()
        # 创建 QTextEdit 并设置充满整个 tab
        layout = QVBoxLayout(tab)
        layout.addWidget(term)
        tab.setLayout(layout)

        # 将新 tab 添加到 tabWidget
        self.ui.tabWidget.addTab(term, cfg['target'])

if __name__ == "__main__":

    app = QApplication()

    # app.setStyle("fusion")
    font = QFont()
    font.setFamilies(["Consolas", "Microsoft YaHei UI"])
    font.setPointSize(10)  # 设置字体大小
    app.setFont(font)

    w = MainWindow()
    w.show()
    app.exec()        