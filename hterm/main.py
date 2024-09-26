from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

import os
import sys
import qtawesome as qta

sys.path.append(os.path.join(os.path.dirname(__file__), 'terminal'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'ui'))

from ui.main_ui import Ui_MainWindow
from common.quick import QuickDialog, QuickButton
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
        self.setWindowTitle("Hterm")
        self.setWindowIcon(QIcon(':/icon.png'))
        self.resize(QGuiApplication.primaryScreen().size()*0.7)
        # self.setWindowOpacity(0.95)

        self.create_session.triggered.connect(lambda: SessionDialog(self).exec())

        # 快速命令按钮
        self.pushButton.setIcon(qta.icon('mdi.speedometer'))
        self.pushButton.setStyleSheet("""
            QPushButton {
                    border: none;
            }   
            QPushButton:hover {
                    background-color: #dddddd;
            }  
        """)
        self.pushButton.clicked.connect(lambda: QuickDialog(self).exec())
        
        self.listWidget.setVisible(False)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(lambda idx: (self.tabWidget.widget(idx).deleteLater(), self.tabWidget.removeTab(idx)))
        # self.tabWidget.setStyleSheet("QTabBar::tab { height: 25px; }")
        
        # 状态栏
        self.statusbar.setStyleSheet("QStatusBar { padding-bottom: 20px; }")
        left_widget = QLabel("就绪")
        self.statusbar.addWidget(left_widget, 1)  # 左侧信息，权重为 1
        button = QPushButton(qta.icon('fa5b.github'), 'Hterm Repository')
        button.setCursor(Qt.PointingHandCursor)
        button.setStyleSheet("""
            QPushButton {
                    color: #5555ff;
                    border: none;
            }   
            QPushButton:hover {
                    color: #5555ff;
                    border: none;
                    text-decoration: underline;
            }  
        """)
        button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl('https://github.com/lbhzy/hterm')))
        self.statusbar.addWidget(button)
        # right_widget = QLabel("2024-8-16 0:11")
        # self.statusbar.addWidget(right_widget, 0)  # 右侧信息，权重为 0

        config = Config("session")
        session_list = config.loadConfig()
        for session in session_list:
            action = QAction(self)
            action.setText(session['name'])
            action.triggered.connect(self.openSession)
            self.session_menu.addAction(action)

        config = Config("quick")
        quick_list = config.loadConfig()
        for quick in quick_list:
            button = QuickButton(quick['type'], quick['content'])
            button.setText(quick['name'])
            button.setIcon(qta.icon('fa.send-o'))
            self.horizontalLayout.insertWidget(1, button)

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
    # font.setPointSize(10)
    app.setFont(font)

    w = MainWindow()
    w.show()
    app.exec()