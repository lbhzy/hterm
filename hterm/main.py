from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

import os
import sys
import qtawesome as qta

sys.path.append(os.path.join(os.path.dirname(__file__), 'terminal'))

from ui.main_ui import Ui_MainWindow
from common.quick import QuickDialog
from common.session import SessionDialog
from common.config import Config
from terminal.terminal_ssh import SSHTerm
from terminal.terminal_local import LocalTerm
from terminal.terminal_serial import SerialTerm



class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):

        super().__init__()
        self.setupUi(self)

        # 主窗口设置
        self.setWindowTitle("hterm")
        self.setWindowIcon(qta.icon('ph.terminal-window-fill'))
        self.resize(QGuiApplication.primaryScreen().size()*0.7)
        # self.setWindowOpacity(0.95)

        self.create_session.triggered.connect(lambda: SessionDialog().exec())

        # 快速命令按钮
        self.toolButton.setIcon(qta.icon('mdi.speedometer'))
        self.toolButton.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.toolButton.clicked.connect(lambda: QuickDialog().exec())
        
        self.listWidget.setVisible(False)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(lambda idx: (self.tabWidget.widget(idx).deleteLater(), self.tabWidget.removeTab(idx)))
        # self.tabWidget.setStyleSheet("QTabBar::tab { height: 25px; }")
        
        # 状态栏
        self.statusbar.setStyleSheet("QStatusBar { padding-bottom: 20px; }")
        left_widget = QLabel("就绪")
        self.statusbar.addWidget(left_widget, 1)  # 左侧信息，权重为 1
        link = QLabel("<a href='https://github.com/lbhzy/hterm'>📬Hterm Repository</a>")
        link.linkActivated.connect(lambda url: QDesktopServices.openUrl(QUrl(url)))
        self.statusbar.addWidget(link)
        # right_widget = QLabel("2024-8-16 0:11")
        # self.statusbar.addWidget(right_widget, 0)  # 右侧信息，权重为 0

        config = Config()
        session_list = config.loadConfig()
        for session in session_list:
            action = QAction(self)
            action.setText(session['name'])
            action.triggered.connect(self.openSession)
            self.session_menu.addAction(action)

        # cfg = config.getConfigByName("openwrt")
        # self.openSession(cfg)
        # cfg = config.getConfigByName("powershell")
        # self.openSession(cfg)

    def openSession(self):
        name = self.sender().text()

        cfg = Config().getConfigByName(name)
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
        self.tabWidget.addTab(term, cfg['target'])

if __name__ == "__main__":

    app = QApplication()

    # app.setStyle("fusion")
    font = QFont()
    font.setFamilies(["Consolas", "Microsoft YaHei UI"])
    # font.setPointSize(10)  # 设置字体大小
    app.setFont(font)

    w = MainWindow()
    w.show()
    app.exec()        