from PySide6.QtGui import *
from PySide6.QtCore import *
from PySide6.QtWidgets import *

import os
import time
import winsound
import pyfiglet
import qtawesome as qta

from vt100 import *
from color import Color
from highlight import Highlighter


class Terminal(QTextEdit, Color, VT100Paser):
    """ 基于QTextEdit实现的终端小部件 """
    def __init__(self):
        super().__init__()

        self.fmt = QTextCharFormat()
        self.pos = [0, 0]
        self.bg_img = f"{os.path.dirname(__file__)}/images/bg1.jpg"

        self.setupUi()
        self.setupSub()

        # 终端语法高亮
        self.highlighter = Highlighter(self.scheme, self.document())

        # self.setLineWrapMode(QTextEdit.WidgetWidth)

        # 快捷键
        self.shortcut_copy = QKeySequence("ALT+C")
        self.shortcut_paste = QKeySequence("ALT+V")
        self.shortcut_clear = QKeySequence("ALT+S")
        self.shortcut_find = QKeySequence("ALT+F")
        self.shortcut_input = QKeySequence("ALT+I")
        QShortcut(self.shortcut_copy, self).activated.connect(lambda: self.copy())
        QShortcut(self.shortcut_paste, self).activated.connect(lambda: self.paste())
        QShortcut(self.shortcut_clear, self).activated.connect(lambda: self.clear())
        QShortcut(self.shortcut_input, self).activated.connect(lambda: self.input())
        QShortcut(self.shortcut_find, self).activated.connect(lambda: self.find())

        # 显示banner
        # banner = pyfiglet.figlet_format("hTerm", font="dos_rebel")
        # self.insertPlainText(banner)
        # print(pyfiglet.FigletFont.getFonts())


    def setupSub(self):
        """ 终端子控件 """
        # QLabel作终端背景图片
        self.background_label = QLabel(self)
        pixmap = QPixmap(self.bg_img)
        size = QGuiApplication.primaryScreen().size()
        pixmap = pixmap.scaled(size, Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        self.background_label.setPixmap(pixmap)
        self.background_label.lower()

        # 查找栏
        self.find_bar = QLineEdit(self)
        self.find_bar.setVisible(False)
        self.find_bar.setGeometry(self.width()-200, 20, 180, 30)
        palette = QPalette()
        palette.setColor(QPalette.Base, QColor(self.scheme['Foreground']))
        palette.setColor(QPalette.Text, QColor(self.scheme['Background']))
        self.find_bar.setPalette(palette)
        self.find_bar.returnPressed.connect(lambda: print(self.find_bar.text()))
        # self.find_bar.show()
        # self.find_bar.setFocus()

        # 输入栏
        self.input_bar = QLineEdit(self)
        self.input_bar.setVisible(False)
        self.input_bar.setPlaceholderText("输入文本，回车发送")
        self.find_bar.setPalette(palette)
        self.input_bar.returnPressed.connect(lambda: (self.sendData(self.input_bar.text()), self.input_bar.clear()))
        self.input_bar.focusOutEvent = lambda _: self.input_bar.hide()

    def setupUi(self):
        """ 终端UI设置 """
        # 设置颜色
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(self.scheme['Background']))
        base_color = QColor(self.scheme['Background'])
        base_color.setAlpha(20)
        palette.setColor(QPalette.Base, base_color)
        palette.setColor(QPalette.Text, QColor(self.scheme['Foreground']))
        self.setPalette(palette)

        # 设置字体
        font = QFont()
        font.setFamilies(["JetBrains Mono", "Consolas", "HarmonyOS Sans SC"])
        # font.setFamilies(["Consolas", "HarmonyOS Sans SC"])
        font.setPointSize(14)
        self.setFont(font)

        # TODO:设置光标样式
        # 隐藏光标
        # self.setCursorWidth(0)  
        # 显示光标
        # self.setCursorWidth(20)

        # 设置图标
        self.setWindowIcon(qta.icon('ph.terminal-window-fill'))
        # self.setWindowIcon(qta.icon('ph.terminal-window-light'))
        
        self.setWindowTitle("Terminal")
        self.setWindowOpacity(0.95)
        self.resize(QGuiApplication.primaryScreen().size()*0.6)
        # 无边框
        # self.setWindowFlags(Qt.FramelessWindowHint)
        # 取消蓝线
        # self.setStyleSheet("QTextEdit::selection { border: 0; background: transparent; }")


    def sendData(self, data):
        """ 需要子类重载 """
        # print(data.encode())
        self.display(data)

    def display(self, text):
        t0 = time.time()
        need_update_scroll_bar = False
        scroll_bar_val = self.verticalScrollBar().value()
        # 开始滚动条就在底部需要更新，开始不在底部保持原始位置
        if scroll_bar_val == self.verticalScrollBar().maximum():
            need_update_scroll_bar = True
        
        info = self.parse(text)

        if need_update_scroll_bar:
            self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
        else:
            self.verticalScrollBar().setValue(scroll_bar_val)
        t1 = time.time()
        # print(f"display cost: {(t1-t0)*1000:.2f}ms ({info})")

    def getExtraSelectedText(self):
        """ 获取选中鼠标文本 """
        selected_text = ""
        for selection in self.extraSelections():
            start = selection.cursor.selectionStart()
            end = selection.cursor.selectionEnd()
            selected_text += self.toPlainText()[start:end]
        return selected_text
    
    # def paintEvent(self, event):
    #     painter = QPainter(self.viewport())
    #     # 根据滚动条位置调整背景图片绘制位置
    #     painter.drawPixmap(self.rect(), self.bg, QRect(0, -self.verticalScrollBar().value(), self.bg.width(), self.bg.height()))
    #     super().paintEvent(event)

    def resizeEvent(self, event: QResizeEvent):
        """ 窗口大小改变事件 """
        ratio = 1
        if self.verticalScrollBar().maximum() > 0:
            ratio = self.verticalScrollBar().value()/self.verticalScrollBar().maximum()
        
        super().resizeEvent(event)

        # 保持滚动条相对位置不变
        val = int(ratio * self.verticalScrollBar().maximum())
        self.verticalScrollBar().setValue(val)

    def inputMethodEvent(self, event: QInputMethodEvent):
        """ 处理输入法输入 """
        self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())

        data = event.commitString()
        if data:
            self.sendData(data)
            position = self.textCursor().position()

        super().inputMethodEvent(event)

        if data:
            # 删除输入法输入的文本
            cursor = self.textCursor()
            cursor.setPosition(cursor.position(), QTextCursor.MoveAnchor)
            cursor.setPosition(position, QTextCursor.KeepAnchor)
            cursor.removeSelectedText()

    def insertFromMimeData(self, source):
        """ 处理粘贴输入 """
        if source.hasText():
            # TODO 多行文本警告
            self.sendData(source.text())
            # 在这里可以对粘贴的文本进行处理
            # processed_text = pasted_text.upper()  # 例如，将粘贴的文本转换为大写
            # self.insertPlainText(processed_text)
        else:
            super().insertFromMimeData(source)

    def keyPressEvent(self, event: QKeyEvent):
        """ 处理键盘输入 """
        text = event.text()

        if event.key() == Qt.Key_Up:        # 上键
            text = '\x1b[A'
        elif event.key() == Qt.Key_Down:    # 下键
            text = '\x1b[B'
        elif event.key() == Qt.Key_Right:   # 右键
            text = '\x1b[C'
        elif event.key() == Qt.Key_Left:    # 左键
            text = '\x1b[D'

        if text:
            self.sendData(text)
            # 用户有输入，定位滚动条到最底部  
            self.verticalScrollBar().setValue(self.verticalScrollBar().maximum())
        else:
            super().keyPressEvent(event)
   
    def wheelEvent(self, event: QWheelEvent):
        """ Ctrl+滚轮 调整字体大小 """
        if event.modifiers() & Qt.ControlModifier:
            font = self.font()
            size = font.pointSize()
            if event.angleDelta().y() > 0:
                size += 1
            else:
                size -= 1
            if size > 0:
                font.setPointSize(size)
                self.setFont(font)
            return
        
        super().wheelEvent(event)

    def mousePressEvent(self, event: QMouseEvent):
        """ 鼠标点击事件 """
        if event.button() == Qt.MiddleButton and event.modifiers() & Qt.ControlModifier:
            font = self.font()
            font.setPointSize(14)
            self.setFont(font)
            return
        if event.button() == Qt.LeftButton:
            if not event.modifiers() & Qt.ControlModifier:
                self.setExtraSelections([])
            cursor = self.cursorForPosition(event.position().toPoint())
            self.left_click_pos = cursor.position()
            return
        if event.button() == Qt.MiddleButton:
            self.paste()
        # super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        """ 双击选中单词行为 """
        self.setExtraSelections([])
        cursor = self.cursorForPosition(event.position().toPoint())
        cursor.select(QTextCursor.WordUnderCursor)

        format = QTextCharFormat()
        format.setBackground(QColor(QColor('#303080')))

        selection = QTextEdit.ExtraSelection()
        selection.format = format
        selection.cursor = cursor
        selections = self.extraSelections()
        selections.append(selection)
        self.setExtraSelections(selections)

    def mouseMoveEvent(self, event: QMouseEvent):
        """ 鼠标移动事件 """
        if event.buttons() & Qt.LeftButton:  # 按住鼠标左键移动
            self.setExtraSelections([])
            format = QTextCharFormat()
            format.setBackground(QColor(0, 0, 180, 200))

            selection = QTextEdit.ExtraSelection()
            selection.format = format
            selection.cursor = self.cursorForPosition(event.position().toPoint())
            selection.cursor.setPosition(self.left_click_pos, QTextCursor.KeepAnchor)
            selections = self.extraSelections()
            selections.append(selection)
            self.setExtraSelections(selections)

        super().mouseMoveEvent(event)

    def copy(self):
        """ 复制操作 """
        text = self.getExtraSelectedText()
        if text:
            clipboard = QClipboard()
            clipboard.setText(text)

    def find(self):
        self.find_bar = QLineEdit(self)
        self.find_bar.setGeometry(self.width()-200, 20, 180, 30)
        palette = QPalette()
        palette.setColor(QPalette.Base, QColor(self.scheme['Foreground']))
        palette.setColor(QPalette.Text, QColor(self.scheme['Background']))
        self.find_bar.setPalette(palette)
        self.find_bar.returnPressed.connect(lambda: print(self.find_bar.text()))
        self.find_bar.show()
        self.find_bar.setFocus()

        self.progress_bar = CircularProgressBar(self)

        self.progress_bar.show()
        # text_to_find = QInputDialog.getText(self, "Find", "Enter text to find:")[0]
        # print(text_to_find)
        # self.find(text_to_find)

    def input(self):
        height = 30
        width = self.width()/1.5
        self.input_bar.setGeometry((self.width()-width)/2, self.height()-height-20, width, height)
        self.input_bar.setVisible(True)
        self.input_bar.setFocus()
        # self.input_bar.setFont(self.font())

    def contextMenuEvent(self, event):
        """ 右键显示菜单 """
        # 选中区域变色
        extra_selected = self.getExtraSelectedText()
        if extra_selected:
            selections = []
            for selection in self.extraSelections():
                selection.format.setBackground(QColor('#5050b0'))
                selections.append(selection)
            self.setExtraSelections(selections)

        clipboard = QApplication.clipboard()
        clipboardhas_content = clipboard.mimeData().hasText()

        menu = QMenu()

        # group1 = menu.addMenu("Group1")
        
        copy_action = QAction("复制", menu)
        # copy_action.setShortcut(QKeySequence.Copy)
        copy_action.setShortcut(self.shortcut_copy)
        copy_action.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditCopy)))
        if not extra_selected:
            copy_action.setDisabled(True)
        
        paste_action = QAction("粘贴", menu)
        paste_action.setShortcut(self.shortcut_paste)
        paste_action.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditPaste)))
        if not clipboardhas_content:
            paste_action.setDisabled(True)

        clear_action = QAction("清除", menu)
        clear_action.setShortcut(self.shortcut_clear)
        clear_action.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditClear)))

        find_action = QAction("查找", menu)
        find_action.setShortcut(self.shortcut_find)
        find_action.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.EditFind)))

        input_action = QAction("输入栏", menu)
        input_action.setShortcut(self.shortcut_input)
        input_action.setIcon(QIcon(QIcon.fromTheme(QIcon.ThemeIcon.DocumentSend)))
        # input_action.setToolTip("通过输入栏输入")
        # input_action.setStyleSheet(f"QAction:hover: QColor(Qt.blue);")


        copy_action.triggered.connect(self.copy)
        paste_action.triggered.connect(self.paste)
        clear_action.triggered.connect(self.clear)
        find_action.triggered.connect(self.find)
        input_action.triggered.connect(self.input)

        menu.addAction(copy_action)
        menu.addAction(paste_action)
        menu.addSeparator()
        menu.addAction(clear_action)
        menu.addAction(find_action)
        menu.addSeparator()
        menu.addAction(input_action)

        menu.exec(event.globalPos()) 
             

    # def focusInEvent(self, e: QFocusEvent) -> None:
    #     self.setInputMethodHints(Qt.ImhPreferLatin)
    #     return super().focusInEvent(e)

    def saveCursorPosition(self):
        cursor=self.textCursor()
        self.pos[0] = cursor.blockNumber()
        # self.pos[1] = cursor.columnNumber()
        self.pos[1] = cursor.positionInBlock()
        # print(f"保存光标位置: {self.pos}")

    def printCursorPosition(self, cursor=None):
        if cursor:
            print(f"光标位置: [{cursor.blockNumber()}, {cursor.positionInBlock()}]")
        else:
            print(f"光标位置: {self.pos}")

    def restoreCursorPosition(self):
        # self.moveCursor(Cursor.SetPosition, pos=(self.pos[0],self.pos[1]))
        cursor = self.textCursor()
        self.setTextCursor(cursor)

    def moveCursorDown(self, cursor, n=1):
        """
        QTextEdit无法将光标移动到不存在的行
        因此向下移动光标需做额外处理
        """
        for _ in range(n):
            if not cursor.movePosition(QTextCursor.Down):
                cursor.select(QTextCursor.LineUnderCursor)
                if cursor.selectedText() == "":
                    # 本行是空行，插入\n
                    self.insertPlainText("\n")
                else:
                    # 本行不是空行，直接append
                    self.append("")
                cursor.clearSelection()
        self.setTextCursor(cursor)

    # 重载转义序列解析器中控制终端的方法
    def updateText(self, text: str):
        position = self.textCursor().position()
        # 更新数据到终端
        self.insertPlainText(text)
        # 删除光标后方数据(只是本行的)，相当于覆盖写入
        cursor = self.textCursor()
        cursor.setPosition(cursor.position(), QTextCursor.MoveAnchor)
        # 本行剩余字符
        remain = cursor.block().length() - 1 - cursor.positionInBlock()
        cnt = min(remain, cursor.position() - position)
        cursor.setPosition(cursor.position()+cnt, QTextCursor.KeepAnchor)
        cursor.removeSelectedText()

    def setDisplayAttributes(self, attrs: list):
        # fmt = self.currentCharFormat()
        fmt = self.fmt
        dim = False
        bright = False
        reverse = False
        hide = False
        for attr in attrs:
            if attr == '' or attr == '0':               # 清除格式
                fmt = QTextCharFormat()
                self.setCurrentCharFormat(fmt)
                self.fmt = fmt
                return
            elif int(attr) >= 30 and int(attr) <= 37:   # 设置文本颜色
                fmt.setForeground(QColor(self.scheme[attr]))
            elif int(attr) >= 40 and int(attr) <= 47:   # 设置文本背景颜色
                fmt.setBackground(QColor(self.scheme[attr]))
            elif attr == '1':           # 明亮的（字体加粗代替）
                bright = True
                fmt.setFontWeight(QFont.Bold)
            elif attr == '2':           # 暗淡的
                dim = True
            elif attr == '4':           # 下划线
                fmt.setFontUnderline(True)
            elif attr == '5':           # 闪烁
                pass    
            elif attr == '7':           # 反显 即前景色和背景色交换
                reverse = True
            elif attr == '8':           # 隐藏
                hide = True
        if dim and not bright:
            color = fmt.foreground().color()
            dim_color = QColor(int(color.red() * 0.8), int(color.green() * 0.8), int(color.blue() * 0.8))
            fmt.setForeground(dim_color)
        elif bright and not dim:
            color = fmt.foreground().color()
            dim_color = QColor(min(255, int(color.red() * 1.2)), min(255, int(color.green() * 1.2)), min(255, int(color.blue() * 1.2)))
            fmt.setForeground(dim_color)

        if reverse:
            fmt.setForeground(QColor(self.scheme["Background"]))
            fmt.setBackground(QColor(self.scheme["Foreground"]))
        if hide:
            fmt.setForeground(QColor(self.scheme["Background"]))

        self.setCurrentCharFormat(fmt)
        self.fmt = fmt
    
    def eraseText(self, action):
        cursor = self.textCursor()
        if action == Erase.Up:
            cursor.setPosition(cursor.position(), QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.Start, QTextCursor.KeepAnchor)
            cursor.removeSelectedText()
        elif action == Erase.Down:
            cursor.setPosition(cursor.position(), QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.End, QTextCursor.KeepAnchor)
            cursor.removeSelectedText()
        elif action == Erase.Line:
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
            cursor.removeSelectedText()
        elif action == Erase.Screen:
            cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.Start, QTextCursor.KeepAnchor)
            cursor.removeSelectedText()
        elif action == Erase.EndofLine:
            cursor.setPosition(cursor.position(), QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            cursor.removeSelectedText()
        elif action == Erase.StartofLine:
            cursor.setPosition(cursor.position(), QTextCursor.MoveAnchor)
            cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.KeepAnchor)
            cursor.removeSelectedText()
        
    def moveCursor(self, action, cnt=1, pos=(0,0)):
        """(row, col)"""
        cursor = self.textCursor()
        position = cursor.position()
        if action == Cursor.Up:
            cursor.movePosition(QTextCursor.Up, n=cnt)
        elif action == Cursor.Down:
            self.moveCursorDown(cursor, cnt)
        elif action == Cursor.Left:
            cursor.movePosition(QTextCursor.Left, n=cnt)
        elif action == Cursor.Right:
            cursor.movePosition(QTextCursor.Right, n=cnt)
        elif action == Cursor.StartOfLine:
            cursor.movePosition(QTextCursor.StartOfLine, n=cnt)
        elif action == Cursor.SetColumn:
            diff = cnt - cursor.block().length()
            if diff >= 0:
                cursor.movePosition(QTextCursor.EndOfLine)
                cursor.insertText(' ' * diff)
            else:
                cursor.setPosition(position - cursor.positionInBlock() + cnt - 1)
        elif action == Cursor.SetPosition:
            cursor.movePosition(QTextCursor.Start)
            self.moveCursorDown(cursor, pos[0])
            cursor.movePosition(QTextCursor.Right, n=pos[1])
        self.setTextCursor(cursor)
        self.setCurrentCharFormat(self.fmt) # 防止文本格式受移动后位置的文本格式影响

    def ringBell(self):
        winsound.PlaySound("SystemHand", winsound.SND_ALIAS | winsound.SND_ASYNC)

if __name__ == "__main__":

    app = QApplication()
    term = Terminal()
    term.show()
    # term.container.show()

    app.exec()
    