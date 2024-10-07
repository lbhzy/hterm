# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QListView, QListWidgetItem,
    QMainWindow, QMenu, QMenuBar, QPushButton,
    QSizePolicy, QSpacerItem, QSplitter, QStatusBar,
    QTabWidget, QVBoxLayout, QWidget)

from session import SessionList
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(794, 517)
        font = QFont()
        font.setPointSize(9)
        MainWindow.setFont(font)
        self.create_session = QAction(MainWindow)
        self.create_session.setObjectName(u"create_session")
        self.setting = QAction(MainWindow)
        self.setting.setObjectName(u"setting")
        self.action1 = QAction(MainWindow)
        self.action1.setObjectName(u"action1")
        self.action1_2 = QAction(MainWindow)
        self.action1_2.setObjectName(u"action1_2")
        self.action2 = QAction(MainWindow)
        self.action2.setObjectName(u"action2")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.splitter.setHandleWidth(0)
        self.listWidget = SessionList(self.splitter)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setMaximumSize(QSize(150, 16777215))
        self.listWidget.setMovement(QListView.Movement.Static)
        self.listWidget.setFlow(QListView.Flow.TopToBottom)
        self.listWidget.setProperty("isWrapping", False)
        self.listWidget.setResizeMode(QListView.ResizeMode.Fixed)
        self.listWidget.setSpacing(1)
        self.listWidget.setViewMode(QListView.ViewMode.ListMode)
        self.splitter.addWidget(self.listWidget)
        self.tabWidget = QTabWidget(self.splitter)
        self.tabWidget.setObjectName(u"tabWidget")
        self.splitter.addWidget(self.tabWidget)

        self.verticalLayout.addWidget(self.splitter)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout.addWidget(self.pushButton)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 794, 33))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.session_menu = QMenu(self.menu)
        self.session_menu.setObjectName(u"session_menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menu.addAction(self.create_session)
        self.menu.addAction(self.session_menu.menuAction())
        self.menu.addSeparator()
        self.menu.addAction(self.setting)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(-1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.create_session.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u4f1a\u8bdd", None))
        self.setting.setText(QCoreApplication.translate("MainWindow", u"\u8bbe\u7f6e...", None))
        self.action1.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.action1_2.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.action2.setText(QCoreApplication.translate("MainWindow", u"2", None))
#if QT_CONFIG(tooltip)
        self.listWidget.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.listWidget.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u5feb\u901f\u547d\u4ee4", None))
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u4f1a\u8bdd", None))
        self.session_menu.setTitle(QCoreApplication.translate("MainWindow", u"\u6240\u6709\u4f1a\u8bdd", None))
    # retranslateUi

