from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *


class CodeEdit(QPlainTextEdit):

    def __init__(self, parent=None):
        super().__init__(parent)
        
        font = QFont()
        font.setFamilies(["Consolas", "Microsoft YaHei UI"])
        font.setPointSize(11)
        self.setFont(font)

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Tab:        # tab
            self.insertPlainText(4 * " ")
        else:
            super().keyPressEvent(event)


if __name__ == '__main__':
    app = QApplication()
    
    edit = CodeEdit()
    edit.show()

    app.exec()