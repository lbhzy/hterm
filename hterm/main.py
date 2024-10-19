from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

import os
import sys
import qtawesome as qta

sys.path.append(os.path.join(os.path.dirname(__file__), 'terminal'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'ui'))

from ui.main_ui import Ui_MainWindow
from common.quick import QuickBar
from common.session import SessionDialog
from common.config import Config
from terminal.terminal_ssh import SSHTerm
from terminal.terminal_local import LocalTerm
from terminal.terminal_serial import SerialTerm
from terminal.terminal_base import Terminal


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):

        super().__init__()
        self.setupUi(self)

        # 主窗口设置
        self.setWindowTitle("Hterm")
        self.setWindowIcon(QIcon(':/icon.png'))
        self.resize(QGuiApplication.primaryScreen().size()*0.7)
        # self.setWindowOpacity(0.95)
        
        # 菜单栏相关
        self.menu.setFocusPolicy(Qt.NoFocus)
        self.session_dialog = SessionDialog(self)
        self.session_dialog.accepted.connect(self.updateSessionMenu)
        self.session_dialog.accepted.connect(self.listWidget.updateSessionList)
        self.create_session.triggered.connect(lambda: self.session_dialog.exec())
        self.updateSessionMenu()
        self.left_action.triggered.connect(lambda check: self.listWidget.setVisible(check))
        self.quicbar_action.triggered.connect(lambda check: self.quick_bar.setVisible(check))
        
        # 快捷命令栏创建
        self.quick_bar = QuickBar(self)
        self.verticalLayout.addWidget(self.quick_bar)
        self.quick_bar.send_signal.connect(self.send2Terminal)

        
        # 会话列表
        self.listWidget.itemDoubleClicked.connect(
            lambda item: self.openSession(self.listWidget.indexFromItem(item).row()))
        self.listWidget.setSpacing(2)
        self.listWidget.update_signal.connect(self.updateSessionMenu)

        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(
            lambda idx: (self.tabWidget.widget(idx).close(), 
                         self.tabWidget.widget(idx).deleteLater(),
                         self.tabWidget.removeTab(idx)))
        # self.tabWidget.setStyleSheet("QTabBar::tab { height: 25px; }")
        
        # 状态栏
        self.statusbar.setStyleSheet("QStatusBar { padding-bottom: 20px; }")
        left_widget = QLabel("🟢就绪")
        self.statusbar.addWidget(left_widget, 1)  # 左侧信息，权重为 1
        button = QPushButton(qta.icon('fa5b.github'), 'Hterm Repository')
        button.setFocusPolicy(Qt.NoFocus)
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
        

    def send2Terminal(self, text):
        term :Terminal = self.tabWidget.currentWidget()
        if term:
            term.preSendData(text)

    def updateSessionMenu(self):
        self.session_menu.clear()
        config = Config("session")
        sessions = config.loadConfig()
        index = 0
        for session in sessions:
            name = session['name'] if session['name'] else session['target']
            action = QAction(self)
            action.setText(name)
            if session['type'] == 'serial':
                action.setIcon(qta.icon('mdi6.serial-port'))
            elif session['type'] == 'ssh':
                action.setIcon(qta.icon('mdi.ssh'))
            elif session['type'] == 'local': 
                action.setIcon(qta.icon('ri.mini-program-line'))
            action.triggered.connect(lambda checked=False, index=index: self.openSession(index))
            self.session_menu.addAction(action)
            index += 1


    def openSession(self, index):
        cfg = Config("session")
        sessions = cfg.loadConfig()
        session = sessions[index]
        if session['type'] == 'ssh':
            term = SSHTerm(session['target'],
                           session['port'],
                           session['username'],
                           session['password'])
        elif session['type'] == 'serial':
            term = SerialTerm(session['target'],session['baudrate'])
        elif session['type'] == 'local':
            term = LocalTerm(session['target'])

        if session['name']:
            name = session['name']
        else:
            name = session['target']

        self.tabWidget.addTab(term, name)
        self.tabWidget.setCurrentIndex(self.tabWidget.indexOf(term))

if __name__ == "__main__":

    app = QApplication()

    app.setStyle("fusion")
    # font = QFont()
    # font.setFamilies(["Consolas", "Microsoft YaHei UI"])
    # font.setPointSize(10)
    # app.setFont(font)

    w = MainWindow()
    w.show()
    app.exec()