from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

from color import Color

class Highlighter(QSyntaxHighlighter):
    """ 语法高亮器 """
    def __init__(self, color, parent=None):
        super(Highlighter, self).__init__(parent)
        self.highlighting_rules = []

        # 命令关键字 - 使用亮绿色
        command_format = QTextCharFormat()
        command_format.setForeground(QColor(color["Green"]))
        # command_pattern = r'\$\s+([^\s]+)|#\s+([^\s]+)'
        command_pattern = r'[#$;|]\s+([^\s]+)'
        self.highlighting_rules.append((QRegularExpression(command_pattern), command_format, "command"))

        # 路径 - 使用亮蓝色
        path_format = QTextCharFormat()
        path_format.setForeground(QColor(color["Blue"]))
        self.highlighting_rules.append((QRegularExpression(r'/\S+'), path_format, "path"))

        # 参数 - 使用亮黄色
        param_format = QTextCharFormat()
        param_format.setForeground(QColor(color["Yellow"]))
        self.highlighting_rules.append((QRegularExpression(r'\s-{1,2}[a-zA-Z]+'), param_format, "param"))

        # 字符串 - 使用亮品红色
        string_format = QTextCharFormat()
        string_format.setForeground(QColor(color["Red"]))
        self.highlighting_rules.append((QRegularExpression(r'[\"\'].*?[\"\']'), string_format, "string"))

        # 用户名/主机名 - 使用青色
        # user_host_format = QTextCharFormat()
        # user_host_format.setForeground(cyan)
        # self.highlighting_rules.append((QRegularExpression(r'\b\w+@[\w.-]+\b'), user_host_format))

        # 异常关键字 - 使用亮红色
        exception_format = QTextCharFormat()
        exception_format.setForeground(QColor(color["Bright Red"]))
        exception_keywords = ["error", "err", "false",
                              "no", "not", "nok",
                              "fail", "failure", "failed"]
        self.highlighting_rules.append((QRegularExpression(r'\b(?:' + '|'.join(exception_keywords) + r')\b', QRegularExpression.CaseInsensitiveOption), exception_format, "exception"))

        # 积极关键字 - 使用亮绿色
        positive_format = QTextCharFormat()
        positive_format.setForeground(QColor(color["Bright Green"]))
        positive_keywords = ["ok", "true",
                              "success", "successful", "successfully"]
        self.highlighting_rules.append((QRegularExpression(r'\b(?:' + '|'.join(positive_keywords) + r')\b', QRegularExpression.CaseInsensitiveOption), positive_format, "positive"))

    def highlightBlock(self, text):
        for pattern, fmt, syntax in self.highlighting_rules:
            expression = QRegularExpression(pattern)
            match = expression.match(text)
            while match.hasMatch():
                if syntax == "command":
                    start = match.capturedStart(1)
                    length = match.capturedLength(1)
                else:
                    start = match.capturedStart()
                    length = match.capturedLength()
                self.setFormat(start, length, fmt)
                match = expression.match(text, start + length)

class MainWindow(QMainWindow):
    def __init__(self, color):
        super(MainWindow, self).__init__()

        self.text_edit = QTextEdit()
        palette = QPalette()
        palette.setColor(QPalette.Base, QColor(color['Background']))
        palette.setColor(QPalette.Text, QColor(color['Foreground']))
        self.setPalette(palette)

        self.highlighter = Highlighter(color, self.text_edit.document())

        self.setCentralWidget(self.text_edit)

        # 测试文本
        self.text_edit.append("cd /home/user")
        self.text_edit.append("mkdir new_folder")
        self.text_edit.append("rm -rf /some/dir")
        self.text_edit.append("sudo apt-get update")
        self.text_edit.append("# This is a comment")
        self.text_edit.append('"This is a string"')
        self.text_edit.append("user@hostname:~$")

        self.text_edit.moveCursor(QTextCursor.End)

if __name__ == "__main__":

    app = QApplication()

    font = QFont()
    font.setFamilies(["Consolas", "Microsoft YaHei UI"])
    font.setPointSize(14)  # 设置字体大小
    app.setFont(font)
    
    window = MainWindow(Color().scheme)
    window.show()
    app.exec()
