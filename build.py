import shutil
from PyInstaller.__main__ import run


def build():
    params = [
        'hterm/main.py',
        '-yw',
        '-i=images/icon.png',
        '-p=hterm/terminal;hterm/ui;hterm/common',
        '--collect-data=winpty',
        '--name=hterm'
    ]
    run(params)

def copy_resources():
    shutil.copytree("hterm/images", "dist/hterm/images")
    shutil.copytree("hterm/schemes", "dist/hterm/schemes")


if __name__ == "__main__":
    build()
    copy_resources()
    