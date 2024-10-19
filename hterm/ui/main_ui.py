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
from PySide6.QtWidgets import (QApplication, QListView, QListWidgetItem, QMainWindow,
    QMenu, QMenuBar, QSizePolicy, QSplitter,
    QStatusBar, QTabWidget, QVBoxLayout, QWidget)

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
        icon = QIcon(QIcon.fromTheme(u"contact-new"))
        self.create_session.setIcon(icon)
        self.setting = QAction(MainWindow)
        self.setting.setObjectName(u"setting")
        icon1 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentProperties))
        self.setting.setIcon(icon1)
        self.action1 = QAction(MainWindow)
        self.action1.setObjectName(u"action1")
        self.action1_2 = QAction(MainWindow)
        self.action1_2.setObjectName(u"action1_2")
        self.action2 = QAction(MainWindow)
        self.action2.setObjectName(u"action2")
        self.about_action = QAction(MainWindow)
        self.about_action.setObjectName(u"about_action")
        icon2 = QIcon(QIcon.fromTheme(u"help-about"))
        self.about_action.setIcon(icon2)
        self.action_2 = QAction(MainWindow)
        self.action_2.setObjectName(u"action_2")
        icon3 = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.NetworkWireless))
        self.action_2.setIcon(icon3)
        self.left_action = QAction(MainWindow)
        self.left_action.setObjectName(u"left_action")
        self.left_action.setCheckable(True)
        self.left_action.setChecked(True)
        self.right_action = QAction(MainWindow)
        self.right_action.setObjectName(u"right_action")
        self.right_action.setCheckable(True)
        self.quicbar_action = QAction(MainWindow)
        self.quicbar_action.setObjectName(u"quicbar_action")
        self.quicbar_action.setCheckable(True)
        self.quicbar_action.setChecked(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(self.centralwidget)
        self.splitter.setObjectName(u"splitter")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(Qt.Orientation.Horizontal)
        self.splitter.setHandleWidth(0)
        self.listWidget = SessionList(self.splitter)
        self.listWidget.setObjectName(u"listWidget")
        self.listWidget.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy1)
        self.listWidget.setMinimumSize(QSize(100, 0))
        self.listWidget.setMaximumSize(QSize(150, 16777215))
        self.listWidget.setBaseSize(QSize(0, 0))
        self.listWidget.setMovement(QListView.Movement.Static)
        self.listWidget.setFlow(QListView.Flow.TopToBottom)
        self.listWidget.setProperty("isWrapping", False)
        self.listWidget.setResizeMode(QListView.ResizeMode.Fixed)
        self.listWidget.setSpacing(1)
        self.listWidget.setViewMode(QListView.ViewMode.ListMode)
        self.splitter.addWidget(self.listWidget)
        self.tabWidget = QTabWidget(self.splitter)
        self.tabWidget.setObjectName(u"tabWidget")
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setMinimumSize(QSize(0, 0))
        self.splitter.addWidget(self.tabWidget)

        self.verticalLayout.addWidget(self.splitter)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 794, 33))
        self.menu = QMenu(self.menubar)
        self.menu.setObjectName(u"menu")
        self.session_menu = QMenu(self.menu)
        self.session_menu.setObjectName(u"session_menu")
        icon4 = QIcon(QIcon.fromTheme(u"address-book-new"))
        self.session_menu.setIcon(icon4)
        self.menu_2 = QMenu(self.menubar)
        self.menu_2.setObjectName(u"menu_2")
        self.menu_3 = QMenu(self.menubar)
        self.menu_3.setObjectName(u"menu_3")
        self.menu_4 = QMenu(self.menubar)
        self.menu_4.setObjectName(u"menu_4")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        self.menubar.addAction(self.menu_4.menuAction())
        self.menu.addAction(self.create_session)
        self.menu.addAction(self.session_menu.menuAction())
        self.menu.addSeparator()
        self.menu.addAction(self.setting)
        self.menu_2.addAction(self.action_2)
        self.menu_3.addAction(self.left_action)
        self.menu_3.addAction(self.right_action)
        self.menu_3.addAction(self.quicbar_action)
        self.menu_4.addAction(self.about_action)

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
        self.about_action.setText(QCoreApplication.translate("MainWindow", u"\u5173\u4e8eHterm", None))
        self.action_2.setText(QCoreApplication.translate("MainWindow", u"\u5c40\u57df\u7f51\u626b\u63cf", None))
        self.left_action.setText(QCoreApplication.translate("MainWindow", u"\u5de6\u4fa7\u680f", None))
        self.right_action.setText(QCoreApplication.translate("MainWindow", u"\u53f3\u4fa7\u680f", None))
        self.quicbar_action.setText(QCoreApplication.translate("MainWindow", u"\u5feb\u901f\u547d\u4ee4\u680f", None))
#if QT_CONFIG(tooltip)
        self.listWidget.setToolTip("")
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(whatsthis)
        self.listWidget.setWhatsThis("")
#endif // QT_CONFIG(whatsthis)
        self.menu.setTitle(QCoreApplication.translate("MainWindow", u"\u4f1a\u8bdd", None))
        self.session_menu.setTitle(QCoreApplication.translate("MainWindow", u"\u6240\u6709\u4f1a\u8bdd", None))
        self.menu_2.setTitle(QCoreApplication.translate("MainWindow", u"\u5de5\u5177", None))
        self.menu_3.setTitle(QCoreApplication.translate("MainWindow", u"\u5e03\u5c40", None))
        self.menu_4.setTitle(QCoreApplication.translate("MainWindow", u"\u5e2e\u52a9", None))
    # retranslateUi

