from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

import os
import re
import sys
import qtawesome as qta

sys.path.append(os.path.join(os.path.dirname(__file__), 'terminal'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'common'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'ui'))

from ui.main_ui import Ui_MainWindow
from common.trigger import Trigger, TriggerDialog
from common.quick import QuickBar
from common.session import SessionDialog
from common.config import Config
from common.setting import SettingDialog
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
        self.setWindowOpacity(0.95)

        # 分离器设置
        self.splitter.setStretchFactor(0, 0)
        self.splitter.setStretchFactor(1, 1)
        self.splitter.setSizes([200, self.width() - 200])
        
        # 菜单栏相关
        self.menu.setFocusPolicy(Qt.NoFocus)
        self.create_session.triggered.connect(self.openSessionDialog)
        self.updateSessionMenu()
        self.left_action.triggered.connect(lambda check: self.listWidget.setVisible(check))
        self.quickbar_action.triggered.connect(lambda check: self.quick_bar.setVisible(check))
        self.statusbar_action.triggered.connect(lambda check: self.statusbar.setVisible(check))
        self.trigger_action.triggered.connect(self.openTriggerDialog)
        self.about_action.triggered.connect(lambda: QMessageBox.information(self, "关于Hterm", "Power by lbhzy"+10*" "))
        self.setting.triggered.connect(lambda: SettingDialog(self).show())

        # 快捷命令栏创建
        self.quick_bar = QuickBar(self)
        self.verticalLayout.addWidget(self.quick_bar)
        self.quick_bar.send_signal.connect(self.send2Session)

        
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
        
    def openSessionDialog(self):
        dialog = SessionDialog(self)
        dialog.accepted.connect(self.updateSessionMenu)
        dialog.accepted.connect(self.listWidget.updateSessionList)
        dialog.exec()

    def openTriggerDialog(self):
        dialog = TriggerDialog(self)
        dialog.accepted.connect(self.updateTrigger)
        dialog.exec()

    def updateTrigger(self):
        for i in range(self.tabWidget.count()):
            term = self.tabWidget.widget(i)
            term.trigger.update()

    def replaceMatch(self, match):
        idx = ord(match.group()[2]) - ord('@')
        return idx.to_bytes().decode()

    def send2Session(self, text, term=None):
        if term == None:
            term: Terminal = self.tabWidget.currentWidget()
        if not term:
            return
        
        text = re.sub(r"\{\^[A-Z]\}", self.replaceMatch, text)
        lines = text.splitlines(True)
        for line in lines:
            text = text[text.find('\n') + 1:] if '\n' in text else text
            if '{delay' in line:
                match = re.search(r'\d+', line)
                if match:
                    delay = int(match.group())
                    timer = QTimer(self)
                    timer.setSingleShot(True)
                    timer.timeout.connect(lambda: self.send2Session(text, term))
                    timer.start(delay)
                    return
                continue

            term.preSendData(line)

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

        
        trigger = Trigger(term)
        term.trigger = trigger
        term.text_added.connect(trigger.text_added)
        trigger.text_send.connect(lambda text: self.send2Session(text, term))
        if session['name']:
            name = session['name']
        else:
            name = session['target']

        self.tabWidget.addTab(term, name)
        self.tabWidget.setCurrentIndex(self.tabWidget.indexOf(term))
        term.setFocus()

if __name__ == "__main__":

    app = QApplication()

    app.setStyle("fusion")
    root_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    font_path = os.path.join(root_path, "fonts")
    with os.scandir(font_path) as entries:
        for entry in entries:
            QFontDatabase.addApplicationFont(entry.path)
    font = QFont()
    font.setFamilies(["Roboto Mono", "HarmonyOS Sans SC"])
    app.setFont(font)

    w = MainWindow()
    w.show()
    app.exec()