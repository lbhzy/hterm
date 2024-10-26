# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'trigger.ui'
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
    QDialogButtonBox, QFormLayout, QHBoxLayout, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QTextEdit, QVBoxLayout, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(856, 555)
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.listWidget = QListWidget(Dialog)
        self.listWidget.setObjectName(u"listWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidget.sizePolicy().hasHeightForWidth())
        self.listWidget.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.listWidget)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.add_button = QPushButton(Dialog)
        self.add_button.setObjectName(u"add_button")

        self.horizontalLayout_2.addWidget(self.add_button)

        self.del_button = QPushButton(Dialog)
        self.del_button.setObjectName(u"del_button")

        self.horizontalLayout_2.addWidget(self.del_button)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.name_edit = QLineEdit(Dialog)
        self.name_edit.setObjectName(u"name_edit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.name_edit)

        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)

        self.pattern_edit = QLineEdit(Dialog)
        self.pattern_edit.setObjectName(u"pattern_edit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.pattern_edit)

        self.label_3 = QLabel(Dialog)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)

        self.action_combobox = QComboBox(Dialog)
        self.action_combobox.addItem("")
        self.action_combobox.setObjectName(u"action_combobox")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.action_combobox)

        self.label_5 = QLabel(Dialog)
        self.label_5.setObjectName(u"label_5")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_5)

        self.textEdit = QTextEdit(Dialog)
        self.textEdit.setObjectName(u"textEdit")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.textEdit)

        self.label_4 = QLabel(Dialog)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.type_combobox = QComboBox(Dialog)
        self.type_combobox.addItem("")
        self.type_combobox.addItem("")
        self.type_combobox.setObjectName(u"type_combobox")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.type_combobox)


        self.horizontalLayout.addLayout(self.formLayout)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.add_button.setText(QCoreApplication.translate("Dialog", u"\u65b0\u589e", None))
        self.del_button.setText(QCoreApplication.translate("Dialog", u"\u5220\u9664", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u540d\u79f0", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"\u5339\u914d", None))
        self.pattern_edit.setPlaceholderText(QCoreApplication.translate("Dialog", u"\u6b63\u5219\u8868\u8fbe\u5f0f", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", u"\u884c\u4e3a", None))
        self.action_combobox.setItemText(0, QCoreApplication.translate("Dialog", u"\u53d1\u9001\u6587\u672c", None))

        self.label_5.setText(QCoreApplication.translate("Dialog", u"\u5185\u5bb9", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", u"\u7c7b\u578b", None))
        self.type_combobox.setItemText(0, QCoreApplication.translate("Dialog", u"\u539f\u59cb\u6587\u672c", None))
        self.type_combobox.setItemText(1, QCoreApplication.translate("Dialog", u"Python\u811a\u672c", None))

    # retranslateUi

