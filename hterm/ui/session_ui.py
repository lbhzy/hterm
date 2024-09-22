# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'session.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFormLayout, QLabel, QLineEdit,
    QSizePolicy, QTabWidget, QVBoxLayout, QWidget)

class Ui_SessionDialog(object):
    def setupUi(self, SessionDialog):
        if not SessionDialog.objectName():
            SessionDialog.setObjectName(u"SessionDialog")
        SessionDialog.resize(673, 443)
        self.verticalLayout = QVBoxLayout(SessionDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(SessionDialog)
        self.tabWidget.setObjectName(u"tabWidget")
        self.ssh_tab = QWidget()
        self.ssh_tab.setObjectName(u"ssh_tab")
        self.formLayoutWidget = QWidget(self.ssh_tab)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(180, 60, 221, 251))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(6)
        self.formLayout.setVerticalSpacing(10)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.ssh_name_label = QLabel(self.formLayoutWidget)
        self.ssh_name_label.setObjectName(u"ssh_name_label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.ssh_name_label)

        self.ssh_name = QLineEdit(self.formLayoutWidget)
        self.ssh_name.setObjectName(u"ssh_name")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.ssh_name)

        self.ssh_server_label = QLabel(self.formLayoutWidget)
        self.ssh_server_label.setObjectName(u"ssh_server_label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.ssh_server_label)

        self.ssh_port_label = QLabel(self.formLayoutWidget)
        self.ssh_port_label.setObjectName(u"ssh_port_label")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.ssh_port_label)

        self.ssh_server = QLineEdit(self.formLayoutWidget)
        self.ssh_server.setObjectName(u"ssh_server")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.ssh_server)

        self.ssh_port = QLineEdit(self.formLayoutWidget)
        self.ssh_port.setObjectName(u"ssh_port")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.ssh_port)

        self.ssh_username_label = QLabel(self.formLayoutWidget)
        self.ssh_username_label.setObjectName(u"ssh_username_label")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.ssh_username_label)

        self.ssh_password_label = QLabel(self.formLayoutWidget)
        self.ssh_password_label.setObjectName(u"ssh_password_label")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.ssh_password_label)

        self.ssh_username = QLineEdit(self.formLayoutWidget)
        self.ssh_username.setObjectName(u"ssh_username")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.ssh_username)

        self.ssh_password = QLineEdit(self.formLayoutWidget)
        self.ssh_password.setObjectName(u"ssh_password")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.ssh_password)

        self.tabWidget.addTab(self.ssh_tab, "")
        self.serial_tab = QWidget()
        self.serial_tab.setObjectName(u"serial_tab")
        self.formLayoutWidget_2 = QWidget(self.serial_tab)
        self.formLayoutWidget_2.setObjectName(u"formLayoutWidget_2")
        self.formLayoutWidget_2.setGeometry(QRect(180, 50, 221, 251))
        self.formLayout_2 = QFormLayout(self.formLayoutWidget_2)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setHorizontalSpacing(6)
        self.formLayout_2.setVerticalSpacing(10)
        self.formLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_6 = QLabel(self.formLayoutWidget_2)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_6)

        self.serial_name = QLineEdit(self.formLayoutWidget_2)
        self.serial_name.setObjectName(u"serial_name")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.serial_name)

        self.label_7 = QLabel(self.formLayoutWidget_2)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.label_7)

        self.serial_port = QComboBox(self.formLayoutWidget_2)
        self.serial_port.setObjectName(u"serial_port")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.serial_port)

        self.label_8 = QLabel(self.formLayoutWidget_2)
        self.label_8.setObjectName(u"label_8")

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.label_8)

        self.serial_baud = QComboBox(self.formLayoutWidget_2)
        self.serial_baud.setObjectName(u"serial_baud")

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.serial_baud)

        self.tabWidget.addTab(self.serial_tab, "")
        self.shell_tab = QWidget()
        self.shell_tab.setObjectName(u"shell_tab")
        self.formLayoutWidget_3 = QWidget(self.shell_tab)
        self.formLayoutWidget_3.setObjectName(u"formLayoutWidget_3")
        self.formLayoutWidget_3.setGeometry(QRect(180, 50, 221, 251))
        self.formLayout_3 = QFormLayout(self.formLayoutWidget_3)
        self.formLayout_3.setObjectName(u"formLayout_3")
        self.formLayout_3.setHorizontalSpacing(6)
        self.formLayout_3.setVerticalSpacing(10)
        self.formLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_9 = QLabel(self.formLayoutWidget_3)
        self.label_9.setObjectName(u"label_9")

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.label_9)

        self.shell_name = QLineEdit(self.formLayoutWidget_3)
        self.shell_name.setObjectName(u"shell_name")

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.shell_name)

        self.label_10 = QLabel(self.formLayoutWidget_3)
        self.label_10.setObjectName(u"label_10")

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.label_10)

        self.shell_program = QLineEdit(self.formLayoutWidget_3)
        self.shell_program.setObjectName(u"shell_program")

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.shell_program)

        self.tabWidget.addTab(self.shell_tab, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.buttonBox = QDialogButtonBox(SessionDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(SessionDialog)
        self.buttonBox.accepted.connect(SessionDialog.accept)
        self.buttonBox.rejected.connect(SessionDialog.reject)

        self.tabWidget.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(SessionDialog)
    # setupUi

    def retranslateUi(self, SessionDialog):
        SessionDialog.setWindowTitle(QCoreApplication.translate("SessionDialog", u"Dialog", None))
        self.ssh_name_label.setText(QCoreApplication.translate("SessionDialog", u"\u540d\u79f0\uff1a", None))
        self.ssh_server_label.setText(QCoreApplication.translate("SessionDialog", u"\u670d\u52a1\u5668\uff1a", None))
        self.ssh_port_label.setText(QCoreApplication.translate("SessionDialog", u"\u7aef\u53e3\u53f7\uff1a", None))
        self.ssh_username_label.setText(QCoreApplication.translate("SessionDialog", u"\u7528\u6237\u540d\uff1a", None))
        self.ssh_password_label.setText(QCoreApplication.translate("SessionDialog", u"\u5bc6\u7801\uff1a", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.ssh_tab), QCoreApplication.translate("SessionDialog", u"SSH", None))
        self.label_6.setText(QCoreApplication.translate("SessionDialog", u"\u540d\u79f0\uff1a", None))
        self.label_7.setText(QCoreApplication.translate("SessionDialog", u"\u4e32\u53e3\uff1a", None))
        self.label_8.setText(QCoreApplication.translate("SessionDialog", u"\u6ce2\u7279\u7387\uff1a", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.serial_tab), QCoreApplication.translate("SessionDialog", u"Serial", None))
        self.label_9.setText(QCoreApplication.translate("SessionDialog", u"\u540d\u79f0\uff1a", None))
        self.label_10.setText(QCoreApplication.translate("SessionDialog", u"\u7a0b\u5e8f\uff1a", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.shell_tab), QCoreApplication.translate("SessionDialog", u"Shell", None))
    # retranslateUi

