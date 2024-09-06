import re
import time
from enum import Enum

class Cursor(Enum):
    """ 终端光标控制 """
    Up          = 1     # 按行数向上移动光标
    Down        = 2     # 按行数向下移动光标
    Left        = 3     # 按列数向左移动光标
    Right       = 4     # 按列数向右移动光标
    StartOfLine = 5     # 移动光标到行首
    SetPosition = 6     # 移动光标到指定（行，列）
    SetRow      = 7     # 移动光标到指定行
    SetColumn   = 8     # 移动光标到指定列

class Erase(Enum):
    """ 擦除终端内容 """
    Up          = 1     # 擦除光标到屏幕顶部内容
    Down        = 2     # 擦除光标到屏幕底部内容
    Line        = 3     # 擦除当前整行的内容
    Screen      = 4     # 擦除整个屏幕
    EndofLine   = 5     # 擦除光标到行尾内容
    StartofLine = 6     # 擦除光标到行首内容

class VT100Paser:
    """ vt100终端控制转义序列解析器 """

    def __init__(self):
        pass

    def parse(self, seq: str):
        """ 解析输入的序列，要求编码格式是utf-8 """
        pattern = r'\x1b\[([?0-9;]*[A-Za-z])|\r|\n|\x08|\a'
        matches = re.finditer(pattern, seq)
        update_text_cost = 0
        control_cost = 0

        last_pos = 0
        for match in matches:
            # print(f"start:{match.start()} end:{match.end()}")
            text = seq[last_pos:match.start()]
            if text:
                t0 = time.time()
                self.updateText(text)
                t1 = time.time()
                update_text_cost += t1-t0
            last_pos = match.end()
            # print(match.group().encode())
            t0 = time.time()
            match match.group():
                case '\r':
                    self.moveCursor(Cursor.StartOfLine)
                case '\n':
                    self.moveCursor(Cursor.Down)
                case '\b':
                    self.moveCursor(Cursor.Left)
                case '\a':
                    self.ringBell()
                case _:
                    self.escapeSeqHandler(match.group(1)[-1:], re.split(";", match.group(1)[:-1]), match.group())
            t1 = time.time()
            control_cost += t1-t0
        text = seq[last_pos:]
        if text:
            t0 = time.time()
            self.updateText(text)
            t1 = time.time()
            update_text_cost += t1-t0
        return f"text:{update_text_cost*1000:.2f}ms control:{control_cost*1000:.2f}ms"


    def escapeSeqHandler(self, flag, argv, match):
        # print(flag, argv)
        match flag:
            # 设置显示属性
            case 'm':
                self.setDisplayAttributes(argv)
            
            # 光标控制
            case 'H'|'f':
                pos = (int(argv[0])-1,int(argv[1])-1) if argv[0] else (0,0)
                self.moveCursor(Cursor.SetPosition, pos=pos)
            case 'A':
                cnt = int(argv[0]) if argv[0] else 1
                self.moveCursor(Cursor.Up, cnt)
            case 'B':
                cnt = int(argv[0]) if argv[0] else 1
                self.moveCursor(Cursor.Down, cnt)
            case 'C':
                cnt = int(argv[0]) if argv[0] else 1
                self.moveCursor(Cursor.Right, cnt)
            case 'D':
                cnt = int(argv[0]) if argv[0] else 1
                self.moveCursor(Cursor.Left, cnt)
            case 'G':
                cnt = int(argv[0]) if argv[0] else 1
                self.moveCursor(Cursor.SetColumn, cnt)
            # 擦除文本
            case 'J':
                if argv[0] == '' or argv[0] == '0':
                    self.eraseText(Erase.Down)
                elif argv[0] == '1':
                    self.eraseText(Erase.Up)
                elif argv[0] == '2':
                    self.eraseText(Erase.Screen) 
            case 'K':
                if argv[0] == '' or argv[0] == '0':
                    self.eraseText(Erase.EndofLine)
                elif argv[0] == '1':
                    self.eraseText(Erase.StartofLine)
                elif argv[0] == '2':
                    self.eraseText(Erase.Line)
            case _:
                pass
                # print(f"Unknown: {match.encode()}")

    # 以下的方法需要终端重载实现
    def updateText(self, text: str):
        print(text)

    def setDisplayAttributes(self, attrs: list):
        print("set attr", attrs)

    def eraseText(self, action):
        print(action)

    def moveCursor(self, action, cnt=1, pos=(0,0)):
        """(row, col)"""
        print(action, cnt, pos)

    def ringBell(self):
        print("ring")


if __name__ == "__main__":

    parser = VT100Paser()

    # ansi_sequence = "Hello\n,\nthis\x1b[5;35;0mis\x1b[mtest\btext\x1b[1;6J"
    ansi_sequence = '\x1b[H\x1b[J\x1b[2;1H~'
    # print(ansi_sequence)
    parser.parse(ansi_sequence)

        
        
        
